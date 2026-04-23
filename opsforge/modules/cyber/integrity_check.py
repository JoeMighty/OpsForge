import click
import hashlib
import os
import json
from opsforge.core.output import console, print_result_table, get_progress

def calculate_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

@click.group(name="integrity-check")
def cmd():
    """Calculates and compares cryptographic hashes of local system files."""
    pass

@cmd.command(name="generate")
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.option("--output", "-o", default="fingerprint.json", help="Output file for hashes")
def generate(directory, output):
    """Generates a fingerprint (hashes) of all files in a directory."""
    console.print(f"[bold cyan]Generating fingerprint for:[/bold cyan] {directory}")
    
    fingerprint = {}
    
    # Walk through directory
    file_list = []
    for root, _, files in os.walk(directory):
        for name in files:
            file_list.append(os.path.join(root, name))

    with get_progress() as progress:
        task = progress.add_task("[cyan]Hashing files...", total=len(file_list))
        for filepath in file_list:
            file_hash = calculate_hash(filepath)
            if file_hash:
                # Store relative path
                rel_path = os.path.relpath(filepath, directory)
                fingerprint[rel_path] = file_hash
            progress.update(task, advance=1)

    try:
        with open(output, "w") as f:
            json.dump(fingerprint, f, indent=4)
        console.print(f"[bold green]Fingerprint saved to:[/bold green] {output}")
    except Exception as e:
        console.print(f"[bold red]Error saving fingerprint:[/bold red] {e}")

@cmd.command(name="verify")
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.argument("fingerprint_file", type=click.Path(exists=True))
def verify(directory, fingerprint_file):
    """Verifies a directory against a previously generated fingerprint."""
    console.print(f"[bold cyan]Verifying directory:[/bold cyan] {directory}")
    
    try:
        with open(fingerprint_file, "r") as f:
            fingerprint = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading fingerprint file:[/bold red] {e}")
        return

    results = []
    found_files = set()

    with get_progress() as progress:
        task = progress.add_task("[cyan]Verifying integrity...", total=len(fingerprint))
        
        for rel_path, expected_hash in fingerprint.items():
            abs_path = os.path.join(directory, rel_path)
            if not os.path.exists(abs_path):
                results.append((rel_path, "MISSING", expected_hash, "N/A"))
            else:
                found_files.add(rel_path)
                actual_hash = calculate_hash(abs_path)
                if actual_hash != expected_hash:
                    results.append((rel_path, "MODIFIED", expected_hash, actual_hash))
            progress.update(task, advance=1)

    # Check for new files not in fingerprint
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            rel_path = os.path.relpath(filepath, directory)
            if rel_path not in fingerprint:
                results.append((rel_path, "NEW", "N/A", calculate_hash(filepath)))

    if results:
        print_result_table(
            "Integrity Violations",
            ["File", "Status", "Expected Hash", "Actual Hash"],
            results
        )
    else:
        console.print("[bold green]Success: Integrity verified. No changes detected.[/bold green]")
