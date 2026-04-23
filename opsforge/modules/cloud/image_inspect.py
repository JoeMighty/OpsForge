import click
import json
import subprocess
from opsforge.core.output import console, print_result_table

@click.command(name="image-inspect")
@click.argument("image_name")
def cmd(image_name):
    """Analyzes Docker images to identify excessively large layers."""
    console.print(f"[bold cyan]Inspecting Docker image:[/bold cyan] {image_name}")
    
    try:
        # Run docker inspect
        result = subprocess.run(
            ["docker", "inspect", image_name],
            capture_output=True, text=True, check=True
        )
        
        data = json.loads(result.stdout)[0]
        
        # Get layers and sizes
        # Note: 'docker inspect' doesn't show individual layer sizes directly in a clean way 
        # unless we use 'docker history'
        
        history_result = subprocess.run(
            ["docker", "history", "--format", "{{.ID}}|{{.Size}}|{{.CreatedBy}}", "--no-trunc", image_name],
            capture_output=True, text=True, check=True
        )
        
        layers = []
        for line in history_result.stdout.strip().split("\n"):
            parts = line.split("|")
            if len(parts) >= 3:
                l_id = parts[0][:12] if "<missing>" not in parts[0] else "BASE"
                size = parts[1]
                cmd = parts[2][:60] + "..." if len(parts[2]) > 60 else parts[2]
                layers.append((l_id, size, cmd))

        print_result_table(
            f"Image Layers: {image_name}",
            ["Layer ID", "Size", "Command"],
            layers
        )

        console.print(f"\n[bold cyan]Metadata:[/bold cyan]")
        console.print(f"  Architecture: {data.get('Architecture')}")
        console.print(f"  OS: {data.get('Os')}")
        console.print(f"  Author: {data.get('Author') or 'N/A'}")

    except subprocess.CalledProcessError:
        console.print("[bold red]Error:[/bold red] Docker is not running or image not found locally.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
