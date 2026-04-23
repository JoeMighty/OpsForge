# Drift Detection Script

The **Drift Detection Script** compares your local infrastructure-as-code state (Terraform `terraform.tfstate` file) against the live deployed resources in your cloud environment. It identifies resources that have been deleted manually via the console or CLI, creating a "drift" from the intended configuration.

## Syntax

```bash
opsforge cloud drift-detect [STATE_FILE]
```

### Arguments
- `STATE_FILE`: Path to the local JSON state file (e.g., `terraform.tfstate`).

## Usage Examples

### Detect drift in a production environment
```bash
opsforge cloud drift-detect ./terraform.tfstate
```

## How It Works
1. It parses the provided JSON state file to extract a list of managed resources, their types, and their unique IDs.
2. For supported resource types, it calls the corresponding AWS API (`ec2:DescribeInstances`, `s3:HeadBucket`, etc.) to verify if the resource still exists in the live environment.
3. It reports the status:
   - **In-Sync**: The resource exists in the live environment as expected.
   - **DRIFTED**: The resource is defined in the state file but could not be found in the live environment (deleted).
   - **Skipped**: The resource type is not yet supported for automated checking.

## Supported Resources
- `aws_instance` (EC2)
- `aws_s3_bucket` (S3)
- `aws_security_group` (NSG)

## Technical Details
This tool uses `boto3` for live environment verification. It implements a read-only check and does not modify any live infrastructure or the state file itself.

> [!IMPORTANT]
> This tool performs a **existence check**. It does not currently detect changes to individual resource attributes (e.g., if an instance type changed from `t2.micro` to `m5.large`). For full attribute-level drift detection, use the `terraform plan` command.
