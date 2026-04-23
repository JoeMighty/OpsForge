import click
import re
from collections import Counter
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="log-analyze")
@click.argument("logfile", type=click.Path(exists=True))
@click.option("--threshold", default=10, help="Threshold for repeated failed logins or high traffic")
def cmd(logfile, threshold):
    """Parses server logs to flag repeated failed logins or traffic spikes."""
    console.print(f"[bold cyan]Analyzing log file:[/bold cyan] {logfile}")

    # Regex for standard Apache/Nginx combined log format
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<date>.*?)\] "(?P<method>\w+) (?P<url>.*?) HTTP/.*?" (?P<status>\d+) (?P<size>\d+)'
    )

    failed_logins = Counter()
    ip_counts = Counter()
    potential_attacks = []

    # Attack patterns
    sqli_pattern = re.compile(r"SELECT|UNION|INSERT|DROP|--|'", re.IGNORECASE)
    xss_pattern = re.compile(r"<script|alert\(|javascript:", re.IGNORECASE)

    try:
        with open(logfile, "r") as f:
            lines = f.readlines()
            
        with get_progress() as progress:
            task = progress.add_task("[cyan]Processing logs...", total=len(lines))
            
            for line in lines:
                match = log_pattern.match(line)
                if match:
                    data = match.groupdict()
                    ip = data["ip"]
                    status = data["status"]
                    url = data["url"]

                    ip_counts[ip] += 1
                    
                    # Track failed logins (401, 403)
                    if status in ["401", "403"]:
                        failed_logins[ip] += 1
                    
                    # Detect potential attacks in URL
                    if sqli_pattern.search(url):
                        potential_attacks.append((ip, "SQL Injection Attempt", url))
                    elif xss_pattern.search(url):
                        potential_attacks.append((ip, "XSS Attempt", url))

                progress.update(task, advance=1)

    except Exception as e:
        console.print(f"[bold red]Error reading log file:[/bold red] {e}")
        return

    # Report results
    console.print("\n[bold yellow]--- Analysis Report ---[/bold yellow]")

    # High Traffic IPs
    high_traffic = [(ip, count) for ip, count in ip_counts.items() if count >= threshold]
    if high_traffic:
        print_result_table("High Traffic IPs", ["IP Address", "Request Count"], high_traffic)
    else:
        console.print("[green]No high traffic IPs detected (threshold: {threshold}).[/green]")

    # Repeated Failed Logins
    repeated_failures = [(ip, count) for ip, count in failed_logins.items() if count >= threshold]
    if repeated_failures:
        print_result_table("Repeated Failed Logins", ["IP Address", "Failure Count"], repeated_failures)
    else:
        console.print("[green]No suspicious failed login patterns detected.[/green]")

    # Potential Attacks
    if potential_attacks:
        print_result_table("Potential Web Attacks", ["IP Address", "Attack Type", "URL Fragment"], potential_attacks[:10])
    else:
        console.print("[green]No obvious SQLi or XSS patterns detected in URLs.[/green]")
