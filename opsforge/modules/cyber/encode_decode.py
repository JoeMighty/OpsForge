import click
import base64
import urllib.parse
from opsforge.core.output import console, print_result_table

@click.group(name="encode-decode")
def cmd():
    """Converts strings between Base64, Hex, and URL encoding formats."""
    pass

@cmd.command(name="base64")
@click.argument("data")
@click.option("--decode", "-d", is_flag=True, help="Decode instead of encode")
def b64(data, decode):
    """Base64 encoding/decoding."""
    try:
        if decode:
            result = base64.b64decode(data).decode("utf-8")
            mode = "Decoded"
        else:
            result = base64.b64encode(data.encode("utf-8")).decode("utf-8")
            mode = "Encoded"
        console.print(f"[bold cyan]{mode} (Base64):[/bold cyan] {result}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cmd.command(name="hex")
@click.argument("data")
@click.option("--decode", "-d", is_flag=True, help="Decode instead of encode")
def hex_codec(data, decode):
    """Hex encoding/decoding."""
    try:
        if decode:
            result = bytes.fromhex(data).decode("utf-8")
            mode = "Decoded"
        else:
            result = data.encode("utf-8").hex()
            mode = "Encoded"
        console.print(f"[bold cyan]{mode} (Hex):[/bold cyan] {result}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@cmd.command(name="url")
@click.argument("data")
@click.option("--decode", "-d", is_flag=True, help="Decode instead of encode")
def url_codec(data, decode):
    """URL encoding/decoding."""
    try:
        if decode:
            result = urllib.parse.unquote(data)
            mode = "Decoded"
        else:
            result = urllib.parse.quote(data)
            mode = "Encoded"
        console.print(f"[bold cyan]{mode} (URL):[/bold cyan] {result}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
