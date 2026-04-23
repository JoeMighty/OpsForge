import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_banner():
    banner = Text("OpsForge", style="bold cyan")
    banner.append("\nConsolidated Toolkit for Cyber & Cloud", style="italic white")
    console.print(Panel(banner, border_style="cyan"))

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """OpsForge: A consolidated toolkit for cybersecurity and cloud infrastructure."""
    pass

@cli.group()
def cyber():
    """Cybersecurity utilities."""
    pass

@cli.group()
def cloud():
    """Cloud infrastructure utilities."""
    pass

# Placeholder for actual tool imports
# from opsforge.modules.cyber import port_scan
# cyber.add_command(port_scan.cmd)

if __name__ == "__main__":
    print_banner()
    cli()
