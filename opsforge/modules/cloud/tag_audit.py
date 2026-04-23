import click
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="tag-audit")
@click.option("--region", "-r", default="us-east-1", help="AWS Region to scan")
@click.option("--mandatory", "-m", default="Project,Owner,Environment", help="Comma-separated mandatory tags")
def cmd(region, mandatory):
    """Scans cloud assets for missing mandatory billing or ownership tags."""
    mandatory_tags = [t.strip() for t in mandatory.split(",")]
    
    console.print(f"[bold cyan]Scanning AWS region:[/bold cyan] {region}")
    console.print(f"[bold cyan]Mandatory tags:[/bold cyan] {', '.join(mandatory_tags)}")
    
    try:
        client = boto3.client('resourcegroupstaggingapi', region_name=region)
        paginator = client.get_paginator('get_resources')
        
        non_compliant = []
        
        # We'll scan all resources
        with get_progress() as progress:
            # We don't know the total number of resources beforehand, 
            # so we use a spinner style or just update as we go.
            task = progress.add_task("[cyan]Retrieving resources...", total=None)
            
            for page in paginator.paginate():
                for resource in page['ResourceTagMappingList']:
                    arn = resource['ResourceARN']
                    tags = {t['Key']: t['Value'] for t in resource['Tags']}
                    
                    missing = [t for t in mandatory_tags if t not in tags]
                    
                    if missing:
                        non_compliant.append((arn, ", ".join(missing)))
                    
                    progress.update(task, advance=1)

        if non_compliant:
            print_result_table(
                "Non-Compliant Resources (Missing Tags)",
                ["Resource ARN", "Missing Tags"],
                non_compliant
            )
        else:
            console.print("[bold green]Success: All scanned resources are compliant.[/bold green]")

    except (BotoCoreError, ClientError) as e:
        console.print(f"[bold red]AWS Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
