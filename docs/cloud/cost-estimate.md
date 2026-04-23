# Cloud Cost Estimator

The **Cloud Cost Estimator** calculates projected monthly costs for common AWS resources using a built-in, offline pricing database. It is designed for quick, back-of-the-envelope calculations without requiring internet access or AWS API connectivity.

## Syntax

```bash
opsforge cloud cost-estimate [COMMAND] [OPTIONS]
```

### Commands

#### `ec2`
Estimate monthly costs for EC2 instances.
- `-i, --instance TEXT`: Instance type (e.g., `t3.micro`).
- `-c, --count INTEGER`: Number of instances.

#### `s3`
Estimate monthly storage costs for S3.
- `-s, --size FLOAT`: Storage size in GB.
- `-t, --tier [standard|infrequent]`: Storage tier.

#### `list`
Lists all available pricing data in the offline database.

## Usage Examples

### Estimate cost for 5 micro instances
```bash
opsforge cloud cost-estimate ec2 -i t3.micro -c 5
```

### Estimate cost for 1 TB of S3 storage
```bash
opsforge cloud cost-estimate s3 --size 1000 --tier standard
```

### View all prices in the database
```bash
opsforge cloud cost-estimate list
```

## Technical Details
This tool uses a hardcoded pricing dictionary (`PRICING_DB`) within the module. Prices are based on the **US-East-1** region and are intended as approximations.

> [!NOTE]
> For precise, up-to-the-minute pricing that includes data transfer, IOPS, and regional variations, always refer to the official **AWS Pricing Calculator**.
