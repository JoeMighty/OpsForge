# Stale Resource Finder

The **Stale Resource Finder** identifies unattached or idle cloud assets in your AWS environment. Finding and removing these resources is a key part of cloud cost optimization and security hygiene.

## Syntax

```bash
opsforge cloud stale-find [OPTIONS]
```

### Options
- `-r, --region TEXT`: AWS region to scan. [default: us-east-1]
- `--help`: Show this message and exit.

## Usage Examples

### Scan for stale resources in the default region
```bash
opsforge cloud stale-find
```

### Scan a different region
```bash
opsforge cloud stale-find -r eu-west-1
```

## Resources Audited

### 1. Unattached EBS Volumes
Scans for EC2 Elastic Block Store (EBS) volumes with a status of `available`. These volumes are not attached to any running or stopped instances and are incurring costs.

### 2. Unassociated Elastic IPs
Identifies Elastic IP addresses (EIPs) that are not associated with any instance or network interface. AWS charges a small hourly fee for unassociated EIPs.

### 3. Idle Load Balancers (ALB/NLB)
Checks Application and Network Load Balancers to see if they have any targets registered in their target groups. An ALB with no targets is usually an abandoned resource that should be deleted.

## Technical Details
This tool uses `boto3` to query the EC2 and ELBv2 APIs. It filters for specific resource states that indicate a "stale" or "idle" condition.

> [!TIP]
> Run this tool monthly as part of your "Cloud Cleanup" routine to significantly reduce unnecessary cloud spend.
