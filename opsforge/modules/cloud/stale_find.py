import click
import boto3
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="stale-find")
@click.option("--region", "-r", default="us-east-1", help="AWS Region to scan")
def cmd(region):
    """Identifies unattached storage volumes or idle load balancers."""
    console.print(f"[bold cyan]Scanning for stale resources in:[/bold cyan] {region}")
    
    stale_resources = []
    
    try:
        # 1. Check for unattached EBS volumes
        ec2 = boto3.client('ec2', region_name=region)
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
        for vol in volumes['Volumes']:
            stale_resources.append((vol['VolumeId'], "EBS Volume", "Available (Unattached)", f"{vol['Size']} GB"))

        # 2. Check for unattached Elastic IPs
        eips = ec2.describe_addresses()
        for eip in eips['Addresses']:
            if 'InstanceId' not in eip and 'NetworkInterfaceId' not in eip:
                stale_resources.append((eip['PublicIp'], "Elastic IP", "Unassociated", "N/A"))

        # 3. Check for idle Load Balancers (ALB/NLB) - No targets registered
        elbv2 = boto3.client('elbv2', region_name=region)
        lbs = elbv2.describe_load_balancers()
        for lb in lbs['LoadBalancers']:
            arn = lb['LoadBalancerArn']
            name = lb['LoadBalancerName']
            
            # Check target groups
            tgs = elbv2.describe_target_groups(LoadBalancerArn=arn)
            has_targets = False
            for tg in tgs['TargetGroups']:
                health = elbv2.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])
                if health['TargetHealthDescriptions']:
                    has_targets = True
                    break
            
            if not has_targets:
                stale_resources.append((name, "Load Balancer", "No Targets", lb['Type']))

        if stale_resources:
            print_result_table(
                "Stale Resources Found",
                ["Resource ID/Name", "Type", "Status", "Details"],
                stale_resources
            )
        else:
            console.print("[bold green]Success: No stale resources detected.[/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
