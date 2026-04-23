import click
import requests
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="fuzzer")
@click.argument("url")
@click.option("--payloads", "-p", help="Path to custom payloads file")
@click.option("--param", default="id", help="Query parameter to fuzz")
def cmd(url, payloads, param):
    """Injects test strings into URLs to check for basic validation flaws."""
    if not url.startswith("http"):
        url = "http://" + url
        
    console.print(f"[bold cyan]Fuzzing target:[/bold cyan] {url}")
    console.print(f"[bold cyan]Target parameter:[/bold cyan] {param}")
    
    if not payloads:
        # Default mini-payload list
        test_payloads = [
            "' OR 1=1 --",
            "<script>alert(1)</script>",
            "../../etc/passwd",
            "'; DROP TABLE users; --",
            "\" OR \"\"=\"",
            "& sleep 10"
        ]
        console.print("[yellow]No payloads file provided. Using default basic test payloads.[/yellow]")
    else:
        try:
            with open(payloads, "r") as f:
                test_payloads = [line.strip() for line in f if line.strip()]
        except Exception as e:
            console.print(f"[bold red]Error reading payloads:[/bold red] {e}")
            return

    results = []

    with get_progress() as progress:
        task = progress.add_task("[cyan]Injecting payloads...", total=len(test_payloads))
        
        for payload in test_payloads:
            try:
                # Prepare params
                params = {param: payload}
                
                # Check original response length/status first if possible, but here we just check for anomalies
                response = requests.get(url, params=params, timeout=10)
                
                # Simple heuristic: if status is 500 or response changed significantly
                results.append((payload, response.status_code, len(response.content)))
            except requests.RequestException as e:
                results.append((payload, "ERROR", str(e)))
            
            progress.update(task, advance=1)

    print_result_table(
        "Fuzzing Results",
        ["Payload", "Status", "Response Size"],
        results
    )
    
    console.print("\n[italic white]Analysis: Look for status 500 (Server Error) or unusual response sizes as indicators of potential vulnerabilities.[/italic white]")
