import click
import os
from jinja2 import Environment, FileSystemLoader
from opsforge.core.output import console

@click.command(name="infra-gen")
@click.option("--type", "-t", type=click.Choice(["terraform"]), default="terraform", help="Type of infrastructure code")
@click.option("--project", "-p", default="opsforge-project", help="Project name")
@click.option("--region", "-r", default="us-east-1", help="AWS Region")
@click.option("--vpc-cidr", default="10.0.0.0/16", help="VPC CIDR block")
@click.option("--output", "-o", default="main.tf", help="Output filename")
def cmd(type, project, region, vpc_cidr, output):
    """Outputs standardized Terraform or CloudFormation templates."""
    console.print(f"[bold cyan]Generating {type} boilerplate for project:[/bold cyan] {project}")
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates")
    
    env = Environment(loader=FileSystemLoader(template_dir))
    
    try:
        if type == "terraform":
            template = env.get_template("terraform_base.j2")
        
        content = template.render(
            project_name=project,
            region=region,
            vpc_cidr=vpc_cidr
        )
        
        with open(output, "w") as f:
            f.write(content)
            
        console.print(f"[bold green]Success: Boilerplate generated at:[/bold green] {output}")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
