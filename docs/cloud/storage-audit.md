# Public Storage Auditor

The **Public Storage Auditor** scans S3 buckets in your AWS account to verify they are not publicly exposed. Publicly readable S3 buckets are one of the most common causes of massive data breaches in the cloud.

## Syntax

```bash
opsforge cloud storage-audit
```

## How It Works
The tool performs a two-layer security check for every bucket in the account:

### 1. Public Access Block (PAB)
Checks if the **S3 Block Public Access** feature is enabled. This is the recommended "master switch" to prevent accidental exposure.
- **Locked**: All four PAB settings are enabled (Best Practice).
- **Partial Block**: Some PAB settings are disabled.
- **No Block Config**: PAB is not configured, meaning the bucket relies solely on ACLs and Policies.

### 2. Bucket ACLs
Analyzes the **Access Control List (ACL)** for each bucket to see if access has been granted to:
- `AllUsers`: Anyone on the internet.
- `AuthenticatedUsers`: Any AWS user (not just those in your account).

## Usage Examples

### Run account-wide audit
```bash
opsforge cloud storage-audit
```

## Technical Details
This tool uses `boto3` to call `s3:ListBuckets`, `s3:GetPublicAccessBlock`, and `s3:GetBucketAcl`. It does not currently audit complex Bucket Policies, as those require more sophisticated semantic analysis.

> [!CAUTION]
> If a bucket is flagged as **EXPOSED**, immediate action is required. Enable "Block Public Access" via the AWS Console or CLI to secure the data.
