import click
import yaml
from opsforge.core.output import console, print_result_table

@click.command(name="pipeline-val")
@click.argument("file", type=click.Path(exists=True))
def cmd(file):
    """Parses YAML files to ensure adherence to testing standards."""
    console.print(f"[bold cyan]Validating CI pipeline file:[/bold cyan] {file}")
    
    try:
        with open(file, "r") as f:
            pipeline = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]Error parsing YAML:[/bold red] {e}")
        return

    findings = []
    
    # 1. Detect platform
    platform = "Unknown"
    if "jobs" in pipeline: platform = "GitHub Actions"
    elif "stages" in pipeline: platform = "GitLab CI"
    
    console.print(f"[bold cyan]Detected Platform:[/bold cyan] {platform}")

    # 2. Check for common security/best practice items
    if platform == "GitHub Actions":
        jobs = pipeline.get("jobs", {})
        for job_name, job_data in jobs.items():
            steps = job_data.get("steps", [])
            
            # Check for 'test' or 'check' step
            has_tests = any("test" in str(step).lower() or "check" in str(step).lower() for step in steps)
            if not has_tests:
                findings.append((job_name, "WARNING", "No 'test' or 'check' steps identified."))
                
            # Check for hardcoded secrets (crude check)
            for step in steps:
                if "run" in step:
                    cmd = step["run"]
                    if any(x in cmd.lower() for x in ["password", "secret", "token"]):
                        if "${{" not in cmd: # Not using GitHub secrets
                            findings.append((job_name, "CRITICAL", f"Potential hardcoded secret in step: {step.get('name', 'unnamed')}"))

    elif platform == "GitLab CI":
        if "test" not in pipeline.get("stages", []):
            findings.append(("Global", "IMPORTANT", "Missing 'test' stage in pipeline definition."))

    if findings:
        print_result_table(
            "Pipeline Validation Findings",
            ["Location", "Severity", "Description"],
            findings
        )
    else:
        console.print("[bold green]Success: Pipeline adheres to basic testing standards.[/bold green]")
