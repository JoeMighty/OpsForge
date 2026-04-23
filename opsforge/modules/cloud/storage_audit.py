import click
import boto3
from botocore.exceptions import ClientError
from opsforge.core.output import console, print_result_table, get_progress

@click.command(name="storage-audit")
def cmd():
    """Scans cloud buckets to verify they are not publicly exposed."""
    console.print("[bold cyan]Auditing S3 Buckets for public exposure...[/bold cyan]")
    
    try:
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        
        results = []
        
        with get_progress() as progress:
            task = progress.add_task("[cyan]Checking buckets...", total=len(buckets['Buckets']))
            
            for bucket in buckets['Buckets']:
                name = bucket['Name']
                public = "[green]Private[/green]"
                reason = "Locked"
                
                try:
                    # 1. Check Public Access Block
                    pab = s3.get_public_access_block(Bucket=name)
                    conf = pab['PublicAccessBlockConfiguration']
                    if not all([conf['BlockPublicAcls'], conf['BlockPublicPolicy'], conf['IgnorePublicAcls'], conf['RestrictPublicBuckets']]):
                        public = "[yellow]Warning[/yellow]"
                        reason = "Partial Block"
                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                        public = "[red]PUBLIC?[/red]"
                        reason = "No Block Config"
                    else:
                        public = "[red]Error[/red]"
                        reason = str(e)

                # 2. Check Bucket ACLs for 'AllUsers' or 'AuthenticatedUsers'
                try:
                    acl = s3.get_bucket_acl(Bucket=name)
                    for grant in acl['Grants']:
                        grantee = grant.get('Grantee', {})
                        uri = grantee.get('URI', '')
                        if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                            public = "[bold red]EXPOSED[/bold red]"
                            reason = f"ACL: {grant['Permission']}"
                            break
                except:
                    pass

                results.append((name, public, reason))
                progress.update(task, advance=1)

        print_result_table("S3 Exposure Audit", ["Bucket Name", "Status", "Reason/Detail"], results)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
