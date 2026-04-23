import click
import requests
from concurrent.futures import ThreadPoolExecutor
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="dir-discover")
@click.argument("url")
@click.option("--wordlist", "-w", type=click.Path(exists=True), help="Path to directory wordlist")
@click.option("--threads", "-t", default=10, help="Number of concurrent threads")
@click.option("--extensions", "-e", default="", help="File extensions to check (e.g., .php,.html)")
def cmd(url, wordlist, threads, extensions):
    """Automates HTTP requests to find hidden web server directories."""
    if not url.startswith("http"):
        url = "http://" + url
    
    console.print(f"[bold cyan]Discovering directories on:[/bold cyan] {url}")
    
    if not wordlist:
        # Default mini-wordlist
        words = ["admin", "login", "config", "backup", "db", "api", "v1", "v2", "upload", "temp", "secret", ".env", ".git"]
        console.print("[yellow]No wordlist provided. Using default common directories.[/yellow]")
    else:
        try:
            with open(wordlist, "r") as f:
                words = [line.strip() for line in f if line.strip()]
        except Exception as e:
            console.print(f"[bold red]Error reading wordlist:[/bold red] {e}")
            return

    ext_list = [ext.strip() for ext in extensions.split(",") if ext.strip()]
    
    # Build target list
    targets = []
    for word in words:
        targets.append(word)
        for ext in ext_list:
            if not ext.startswith("."):
                ext = "." + ext
            targets.append(f"{word}{ext}")

    found_items = []

    def check_dir(item):
        target_url = f"{url.rstrip('/')}/{item}"
        try:
            # Use head request first for speed
            response = requests.head(target_url, allow_redirects=True, timeout=5)
            if response.status_code != 404:
                return item, response.status_code, len(response.content)
        except requests.RequestException:
            pass
        return None

    with get_progress() as progress:
        task = progress.add_task("[cyan]Brute-forcing directories...", total=len(targets))
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(check_dir, t) for t in targets]
            for future in futures:
                res = future.result()
                if res:
                    found_items.append(res)
                progress.update(task, advance=1)

    if found_items:
        print_result_table(
            f"Found Directories/Files on {url}",
            ["Item", "Status Code", "Size"],
            found_items
        )
    else:
        console.print("[yellow]No hidden directories or files found.[/yellow]")
