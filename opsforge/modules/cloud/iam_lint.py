import click
import json
from opsforge.core.output import console, print_result_table

@click.command(name="iam-lint")
@click.argument("file", type=click.Path(exists=True))
def cmd(file):
    """Evaluates JSON IAM documents for overly permissive access rules."""
    console.print(f"[bold cyan]Linting IAM policy file:[/bold cyan] {file}")
    
    try:
        with open(file, "r") as f:
            policy = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error parsing JSON:[/bold red] {e}")
        return

    findings = []
    
    statements = policy.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
        
    for i, stmt in enumerate(statements):
        effect = stmt.get("Effect")
        action = stmt.get("Action", [])
        resource = stmt.get("Resource", [])
        
        # Normalize to lists
        if isinstance(action, str): action = [action]
        if isinstance(resource, str): resource = [resource]
        
        if effect == "Allow":
            # Check for full admin action
            if "*" in action:
                findings.append((f"Stmt[{i}]", "CRITICAL", "Full Action wildcard ('*') allowed."))
            
            # Check for resource wildcard
            if "*" in resource:
                findings.append((f"Stmt[{i}]", "WARNING", "Full Resource wildcard ('*') allowed."))
                
            # Check for dangerous actions (simple list)
            dangerous_actions = ["iam:*", "s3:DeleteBucket", "ec2:TerminateInstances"]
            for da in dangerous_actions:
                if da in action:
                    findings.append((f"Stmt[{i}]", "IMPORTANT", f"Dangerous action detected: {da}"))

    if findings:
        print_result_table(
            "IAM Policy Findings",
            ["Location", "Severity", "Description"],
            findings
        )
    else:
        console.print("[bold green]Success: No major issues found in the IAM policy.[/bold green]")
