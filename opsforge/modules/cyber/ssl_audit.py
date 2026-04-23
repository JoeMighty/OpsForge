import click
import socket
import ssl
from datetime import datetime
from opsforge.core.output import console, print_result_table

@click.command(name="ssl-audit")
@click.argument("hostname")
@click.option("--port", "-p", default=443, help="Port to check")
def cmd(hostname, port):
    """Checks SSL certificate expiration dates and cryptographic algorithms."""
    console.print(f"[bold cyan]Auditing SSL certificate for:[/bold cyan] {hostname}:{port}")
    
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()

        # Parse expiration
        not_after_str = cert['notAfter']
        expires = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
        days_left = (expires - datetime.now()).days

        # Parse issuer
        issuer = dict(x[0] for x in cert['issuer'])
        common_name = issuer.get('commonName', 'Unknown')

        results = [
            ("Status", "[bold green]Valid[/bold green]" if days_left > 0 else "[bold red]Expired[/bold red]"),
            ("Subject", dict(x[0] for x in cert['subject']).get('commonName', 'Unknown')),
            ("Issuer", common_name),
            ("Expires", f"{not_after_str} ({days_left} days left)"),
            ("Protocol", version),
            ("Cipher", cipher[0]),
            ("Key Bits", cipher[2])
        ]

        print_result_table(f"SSL Audit: {hostname}", ["Metric", "Value"], results)

        if days_left < 30:
            console.print(f"[bold yellow]Warning: Certificate expires in {days_left} days.[/bold yellow]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
