import click
import requests
import time
from opsforge.core.output import console, print_result_table

@click.command(name="uptime-monitor")
@click.argument("urls", nargs=-1)
@click.option("--interval", "-i", default=60, help="Interval between checks in seconds")
@click.option("--count", "-c", default=1, help="Number of checks to perform (0 for infinite)")
def cmd(urls, interval, count):
    """Pings cloud endpoints and alerts on non-200 status codes."""
    if not urls:
        console.print("[bold red]Error:[/bold red] No URLs provided.")
        return

    console.print(f"[bold cyan]Starting Uptime Monitor...[/bold cyan]")
    console.print(f"[bold cyan]Target URLs:[/bold cyan] {', '.join(urls)}")
    console.print(f"[bold cyan]Interval:[/bold cyan] {interval}s")
    
    check_num = 0
    while True:
        check_num += 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        results = []
        
        for url in urls:
            if not url.startswith("http"):
                url = "http://" + url
            
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                latency = (time.time() - start_time) * 1000
                
                status = f"[green]{response.status_code}[/green]" if response.status_code == 200 else f"[red]{response.status_code}[/red]"
                results.append((url, status, f"{latency:.2f} ms"))
                
                if response.status_code != 200:
                    console.print(f"[bold red]ALERT:[/bold red] {url} returned status {response.status_code} at {timestamp}")
            except Exception as e:
                results.append((url, "[bold red]DOWN[/bold red]", str(e)))
                console.print(f"[bold red]ALERT:[/bold red] {url} is UNREACHABLE at {timestamp}")

        console.print(f"\n[bold yellow]Check #{check_num} at {timestamp}[/bold yellow]")
        print_result_table("Uptime Status", ["URL", "Status", "Latency/Error"], results)
        
        if count > 0 and check_num >= count:
            break
            
        time.sleep(interval)
