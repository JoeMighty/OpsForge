# Resource Tagging Auditor

The **Resource Tagging Auditor** scans AWS assets to identify resources that are missing mandatory billing or ownership tags. This is essential for cost allocation, security ownership, and organizational compliance.

## Syntax

```bash
opsforge cloud tag-audit [OPTIONS]
```

### Options
- `-r, --region TEXT`: AWS region to scan. [default: us-east-1]
- `-m, --mandatory TEXT`: Comma-separated list of mandatory tag keys. [default: Project,Owner,Environment]
- `--help`: Show this message and exit.

## Usage Examples

### Scan default region with default tags
```bash
opsforge cloud tag-audit
```

### Scan a specific region with custom mandatory tags
```bash
opsforge cloud tag-audit -r us-west-2 -m CostCenter,Dept,AppID
```

## Technical Details
This tool utilizes the **AWS Resource Groups Tagging API** (`get_resources`) via `boto3`. It iterates through all supported resources in the specified region and compares their attached tags against the provided mandatory list.

> [!IMPORTANT]
> **Authentication**: This tool requires valid AWS credentials configured on your system (e.g., via `~/.aws/credentials` or environment variables like `AWS_ACCESS_KEY_ID`).
> **Permissions**: The IAM identity used must have the `tag:GetResources` permission.

## Why Tagging Matters?
- **Billing**: Categorize costs by project or environment.
- **Automation**: Target specific resources for automated backup or patching.
- **Security**: Identify which team or individual is responsible for a specific asset.
