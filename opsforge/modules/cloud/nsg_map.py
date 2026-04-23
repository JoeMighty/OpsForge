import click
import boto3
import csv
from opsforge.core.output import console, print_result_table

@click.command(name="nsg-map")
@click.option("--region", "-r", default="us-east-1", help="AWS Region to scan")
@click.option("--output", "-o", help="Output CSV filename")
def cmd(region, output):
    """Extracts cloud firewall rules (Security Groups) into a readable format."""
    console.print(f"[bold cyan]Mapping Security Groups in:[/bold cyan] {region}")
    
    try:
        ec2 = boto3.client('ec2', region_name=region)
        sgs = ec2.describe_security_groups()
        
        rules = []
        
        for sg in sgs['SecurityGroups']:
            sg_name = sg.get('GroupName', 'N/A')
            sg_id = sg['GroupId']
            
            for rule in sg['IpPermissions']:
                proto = rule.get('IpProtocol', 'all')
                from_port = rule.get('FromPort', 'all')
                to_port = rule.get('ToPort', 'all')
                
                # Extract CIDR ranges
                for ip_range in rule.get('IpRanges', []):
                    cidr = ip_range.get('CidrIp')
                    rules.append((sg_name, sg_id, "Ingress", proto, f"{from_port}-{to_port}", cidr))
                
                # Extract Group IDs (Source SGs)
                for group in rule.get('UserIdGroupPairs', []):
                    src_sg = group.get('GroupId')
                    rules.append((sg_name, sg_id, "Ingress", proto, f"{from_port}-{to_port}", src_sg))

        if not rules:
            console.print("[yellow]No rules found.[/yellow]")
            return

        if output:
            with open(output, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["SG Name", "SG ID", "Type", "Protocol", "Ports", "Source"])
                writer.writerows(rules)
            console.print(f"[bold green]Rules exported to:[/bold green] {output}")
        else:
            print_result_table(
                "Security Group Rules",
                ["SG Name", "SG ID", "Dir", "Proto", "Ports", "Source"],
                rules[:20] # Show first 20 in console
            )
            if len(rules) > 20:
                console.print(f"\n[italic white]Showing first 20 of {len(rules)} rules. Use --output to save all to CSV.[/italic white]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
