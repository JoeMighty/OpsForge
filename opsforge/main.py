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

from opsforge.modules.cyber import (
    port_scan, log_analyze, integrity_check, 
    subdomain_enum, password_check, packet_sniff,
    encode_decode, dir_discover, ssl_audit, honeypot,
    fuzzer
)
from opsforge.modules.cloud import (
    tag_audit, iam_lint, infra_gen, stale_find,
    nsg_map, storage_audit, image_inspect, uptime_monitor,
    pipeline_val, cost_estimate, drift_detect
)

cyber.add_command(port_scan.cmd)
cyber.add_command(log_analyze.cmd)
cyber.add_command(integrity_check.cmd)
cyber.add_command(subdomain_enum.cmd)
cyber.add_command(password_check.cmd)
cyber.add_command(packet_sniff.cmd)
cyber.add_command(encode_decode.cmd)
cyber.add_command(dir_discover.cmd)
cyber.add_command(ssl_audit.cmd)
cyber.add_command(honeypot.cmd)
cyber.add_command(fuzzer.cmd)

cloud.add_command(tag_audit.cmd)
cloud.add_command(iam_lint.cmd)
cloud.add_command(infra_gen.cmd)
cloud.add_command(stale_find.cmd)
cloud.add_command(nsg_map.cmd)
cloud.add_command(storage_audit.cmd)
cloud.add_command(image_inspect.cmd)
cloud.add_command(uptime_monitor.cmd)
cloud.add_command(pipeline_val.cmd)
cloud.add_command(cost_estimate.cmd)
cloud.add_command(drift_detect.cmd)

if __name__ == "__main__":
    print_banner()
    cli()
