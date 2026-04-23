import click
from opsforge.core.output import console, print_result_table

# Offline static pricing data (Sample - Monthly costs for US-East-1)
PRICING_DB = {
    "ec2": {
        "t3.nano": 3.80,
        "t3.micro": 7.59,
        "t3.small": 15.18,
        "t3.medium": 30.37,
        "m5.large": 70.08,
        "m5.xlarge": 140.16,
    },
    "s3": {
        "standard_gb": 0.023,
        "infrequent_gb": 0.0125,
    },
    "rds": {
        "db.t3.micro": 12.41,
        "db.t3.small": 24.82,
        "db.m5.large": 124.10,
    }
}

@click.group(name="cost-estimate")
def cmd():
    """Calculates projected costs using offline static pricing data."""
    pass

@cmd.command(name="ec2")
@click.option("--instance", "-i", default="t3.micro", help="Instance type")
@click.option("--count", "-c", default=1, help="Number of instances")
def ec2_cost(instance, count):
    """Estimate EC2 monthly costs."""
    price = PRICING_DB["ec2"].get(instance)
    if not price:
        console.print(f"[bold red]Error:[/bold red] Instance type {instance} not found in offline DB.")
        return
    
    total = price * count
    console.print(f"[bold cyan]Projected Monthly Cost for {count}x {instance}:[/bold cyan] ${total:.2f}")

@cmd.command(name="s3")
@click.option("--size", "-s", required=True, type=float, help="Storage size in GB")
@click.option("--tier", "-t", type=click.Choice(["standard", "infrequent"]), default="standard")
def s3_cost(size, tier):
    """Estimate S3 monthly storage costs."""
    price_key = f"{tier}_gb"
    price = PRICING_DB["s3"].get(price_key)
    
    total = price * size
    console.print(f"[bold cyan]Projected Monthly Cost for {size} GB ({tier}):[/bold cyan] ${total:.2f}")

@cmd.command(name="list")
def list_prices():
    """Lists all available pricing data in the offline DB."""
    rows = []
    for category, items in PRICING_DB.items():
        for name, price in items.items():
            rows.append((category.upper(), name, f"${price}"))
    
    print_result_table("Offline Pricing Database (US-East-1)", ["Category", "Item", "Monthly Price"], rows)
