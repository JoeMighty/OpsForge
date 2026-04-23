# Cloud Infrastructure Utilities

The **Cloud** module of OpsForge provides a suite of 11 tools designed for auditing, monitoring, and managing cloud infrastructure, with a primary focus on AWS.

## Available Tools

| Tool | Functionality |
| --- | --- |
| [Tag Auditor](tag-audit.md) | Scans for missing mandatory resource tags. |
| [IAM Linter](iam-lint.md) | Evaluates IAM policies for permissive rules. |
| [Infra Generator](infra-gen.md) | Generates Terraform/CloudFormation templates. |
| [Stale Resource Finder](stale-find.md) | Identifies idle or unattached cloud assets. |
| [NSG Rule Mapper](nsg-map.md) | Maps firewall rules to spreadsheets. |
| [Storage Auditor](storage-audit.md) | Verifies public storage exposure (S3). |
| [Image Inspector](image-inspect.md) | Analyzes Docker image layers. |
| [Uptime Monitor](uptime-monitor.md) | Pings endpoints for health checks. |
| [Pipeline Validator](pipeline-val.md) | Linters for CI/CD YAML files. |
| [Cost Estimator](cost-estimate.md) | Calculates projected costs offline. |
| [Drift Detector](drift-detect.md) | Compares code vs live infrastructure. |
