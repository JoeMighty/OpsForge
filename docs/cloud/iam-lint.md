# IAM Policy Linter

The **IAM Policy Linter** evaluates AWS Identity and Access Management (IAM) JSON policy documents for security anti-patterns and overly permissive access rules. It helps enforce the **Principle of Least Privilege (PoLP)**.

## Syntax

```bash
opsforge cloud iam-lint [FILE]
```

### Arguments
- `FILE`: Path to the IAM policy JSON file to audit.

## Usage Examples

### Audit a local policy file
```bash
opsforge cloud iam-lint my_policy.json
```

## Security Checks
The tool scans for the following high-risk patterns:
- **Action Wildcard (`*`)**: Grants access to all actions within a service or across all services if used as `*`. This is flagged as `CRITICAL`.
- **Resource Wildcard (`*`)**: Grants access to all resources. This is often necessary but should be scrutinized for sensitive services. Flagged as `WARNING`.
- **Dangerous Actions**: Specifically looks for high-impact actions like `iam:*`, `s3:DeleteBucket`, and `ec2:TerminateInstances`. Flagged as `IMPORTANT`.

## Technical Details
This tool is an **offline** validator. It does not communicate with the AWS API; it parses and analyzes the provided JSON file locally using logic-based heuristics.

> [!CAUTION]
> An IAM policy that passes this linter is not necessarily "secure" in your specific context, but it is free from common, glaring security flaws. Always perform a manual review for mission-critical policies.
