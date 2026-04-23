import click
from scapy.all import sniff, IP, TCP, UDP, Raw
from opsforge.core.output import console

@click.command(name="packet-sniff")
@click.option("--iface", "-i", help="Interface to sniff on (e.g., eth0, wlan0)")
@click.option("--count", "-c", default=10, help="Number of packets to capture")
@click.option("--filter", "-f", default="", help="BPF filter (e.g., 'tcp and port 80')")
def cmd(iface, count, filter):
    """Captures and decodes local network traffic headers and payloads."""
    console.print(f"[bold cyan]Starting packet sniffer on interface:[/bold cyan] {iface or 'default'}")
    if filter:
        console.print(f"[bold cyan]Filter:[/bold cyan] {filter}")
    
    console.print("[yellow]Note: This tool usually requires administrative/root privileges.[/yellow]\n")

    def packet_callback(packet):
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "OTHER"
            
            payload_info = ""
            if Raw in packet:
                payload = packet[Raw].load
                # Show first 50 chars of hex/text
                payload_info = f" | Payload: {payload[:50].hex()}"

            console.print(f"[green][{proto}][/green] {ip_src} -> {ip_dst}{payload_info}")

    try:
        sniff(iface=iface, count=count, filter=filter, prn=packet_callback, store=0)
    except PermissionError:
        console.print("[bold red]Error:[/bold red] Permission denied. Please run as administrator/root.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

    console.print(f"\n[bold green]Capture of {count} packets complete.[/bold green]")
