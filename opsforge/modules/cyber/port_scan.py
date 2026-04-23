import click
import socket
from concurrent.futures import ThreadPoolExecutor
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="port-scan")
@click.argument("target")
@click.option("--ports", "-p", default="1-1024", help="Port range (e.g., 80,443 or 1-1024)")
@click.option("--threads", "-t", default=50, help="Number of concurrent threads")
@click.option("--timeout", default=1.0, help="Socket timeout in seconds")
def cmd(target, ports, threads, timeout):
    """Probes IP addresses for open ports using raw socket connections."""
    console.print(f"[bold cyan]Scanning target:[/bold cyan] {target}")
    
    # Parse port range
    target_ports = []
    try:
        if "-" in ports:
            start, end = map(int, ports.split("-"))
            target_ports = list(range(start, end + 1))
        else:
            target_ports = [int(p) for p in ports.split(",")]
    except ValueError:
        console.print("[bold red]Error:[/bold red] Invalid port range format.")
        return

    open_ports = []
    
    def check_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return port, service
        return None

    with get_progress() as progress:
        task = progress.add_task("[cyan]Scanning ports...", total=len(target_ports))
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(check_port, p) for p in target_ports]
            for future in futures:
                res = future.result()
                if res:
                    open_ports.append(res)
                progress.update(task, advance=1)

    if open_ports:
        print_result_table(
            f"Open Ports on {target}",
            ["Port", "Service"],
            open_ports
        )
    else:
        console.print("[yellow]No open ports found.[/yellow]")
