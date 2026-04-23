import click
import math
from opsforge.core.output import console, print_result_table

def calculate_entropy(password):
    """Calculates the Shannon entropy of a password."""
    if not password:
        return 0
    
    # Determine the character set size (L)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    l = 0
    if has_lower: l += 26
    if has_upper: l += 26
    if has_digit: l += 10
    if has_special: l += 32 # Approximate count of special chars
    
    # Entropy = Length * log2(L)
    entropy = len(password) * math.log2(l) if l > 0 else 0
    return entropy

@click.command(name="password-check")
@click.argument("password", required=False)
@click.option("--interactive", "-i", is_flag=True, help="Prompt for password (safer)")
def cmd(password, interactive):
    """Evaluates the mathematical strength of passwords offline."""
    if interactive:
        password = click.prompt("Enter password to check", hide_input=True)
    
    if not password:
        console.print("[bold red]Error:[/bold red] No password provided.")
        return

    entropy = calculate_entropy(password)
    
    # Determine strength
    if entropy < 40:
        strength = "[bold red]Very Weak[/bold red]"
    elif entropy < 60:
        strength = "[red]Weak[/red]"
    elif entropy < 80:
        strength = "[yellow]Moderate[/yellow]"
    elif entropy < 100:
        strength = "[green]Strong[/green]"
    else:
        strength = "[bold green]Very Strong[/bold green]"

    print_result_table(
        "Password Strength Analysis",
        ["Metric", "Value"],
        [
            ("Length", len(password)),
            ("Entropy (bits)", f"{entropy:.2f}"),
            ("Rating", strength)
        ]
    )

    console.print("\n[italic white]Note: Higher entropy (bits) indicates better resistance to brute-force attacks.[/italic white]")
