import click
import json
import boto3
from botocore.exceptions import ClientError
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="drift-detect")
@click.argument("state_file", type=click.Path(exists=True))
def cmd(state_file):
    """Compares local config code (state) against live deployed infrastructure."""
    console.print(f"[bold cyan]Performing drift detection using state file:[/bold cyan] {state_file}")
    
    try:
        with open(state_file, "r") as f:
            state = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error parsing state file:[/bold red] {e}")
        return

    resources = state.get("resources", [])
    findings = []
    
    with get_progress() as progress:
        task = progress.add_task("[cyan]Checking live resources...", total=len(resources))
        
        for res in resources:
            res_type = res.get("type")
            instances = res.get("instances", [])
            
            for inst in instances:
                attr = inst.get("attributes", {})
                res_id = attr.get("id") or attr.get("arn") or "unknown"
                
                status = "[green]In-Sync[/green]"
                detail = "Found"

                # Simplified check: verify resource existence via AWS API
                try:
                    if res_type == "aws_instance":
                        ec2 = boto3.client('ec2')
                        ec2.describe_instances(InstanceIds=[res_id])
                    elif res_type == "aws_s3_bucket":
                        s3 = boto3.client('s3')
                        s3.head_bucket(Bucket=res_id)
                    elif res_type == "aws_security_group":
                        ec2 = boto3.client('ec2')
                        ec2.describe_security_groups(GroupIds=[res_id])
                    else:
                        status = "[yellow]Skipped[/yellow]"
                        detail = f"Unsupported type: {res_type}"
                except ClientError as e:
                    if "NotFound" in str(e) or "404" in str(e):
                        status = "[bold red]DRIFTED[/bold red]"
                        detail = "Resource missing in AWS"
                    else:
                        status = "[red]Error[/red]"
                        detail = str(e)
                except Exception as e:
                    status = "[red]Error[/red]"
                    detail = str(e)

                findings.append((res_type, res_id, status, detail))
            
            progress.update(task, advance=1)

    print_result_table(
        "Drift Detection Results",
        ["Type", "Resource ID", "Status", "Details"],
        findings
    )
