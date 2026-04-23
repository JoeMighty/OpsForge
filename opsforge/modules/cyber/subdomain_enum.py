import click
import socket
from concurrent.futures import ThreadPoolExecutor
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="subdomain-enum")
@click.argument("domain")
@click.option("--wordlist", "-w", type=click.Path(exists=True), help="Path to subdomain wordlist")
@click.option("--threads", "-t", default=20, help="Number of concurrent threads")
def cmd(domain, wordlist, threads):
    """Queries DNS records to map the external attack surface."""
    console.print(f"[bold cyan]Enumerating subdomains for:[/bold cyan] {domain}")
    
    if not wordlist:
        # Default mini-wordlist if none provided
        subdomains = ["www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2", "smtp", "vpn", "m", "shop", "ftp", "autodiscover", "dev", "staging"]
        console.print("[yellow]No wordlist provided. Using default common subdomains.[/yellow]")
    else:
        try:
            with open(wordlist, "r") as f:
                subdomains = [line.strip() for line in f if line.strip()]
        except Exception as e:
            console.print(f"[bold red]Error reading wordlist:[/bold red] {e}")
            return

    found_subdomains = []

    def check_subdomain(sub):
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            return target, ip
        except socket.gaierror:
            return None

    with get_progress() as progress:
        task = progress.add_task("[cyan]Resolving DNS...", total=len(subdomains))
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(check_subdomain, s) for s in subdomains]
            for future in futures:
                res = future.result()
                if res:
                    found_subdomains.append(res)
                progress.update(task, advance=1)

    if found_subdomains:
        print_result_table(
            f"Found Subdomains for {domain}",
            ["Subdomain", "IP Address"],
            found_subdomains
        )
    else:
        console.print("[yellow]No subdomains found.[/yellow]")
