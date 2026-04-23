# NSG Rule Mapper

The **NSG Rule Mapper** extracts and flattens cloud firewall rules (AWS Security Groups) into a readable format. It helps security auditors quickly visualize the ingress and egress rules across a large number of security groups.

## Syntax

```bash
opsforge cloud nsg-map [OPTIONS]
```

### Options
- `-r, --region TEXT`: AWS region to scan. [default: us-east-1]
- `-o, --output PATH`: Output CSV filename to save all rules.
- `--help`: Show this message and exit.

## Usage Examples

### Preview rules in the console
```bash
opsforge cloud nsg-map
```

### Export all rules to a CSV file
```bash
opsforge cloud nsg-map -o sg_audit.csv
```

## Data Extracted
For every security group rule, the tool extracts:
- **SG Name**: The descriptive name of the Security Group.
- **SG ID**: The unique AWS identifier for the Security Group.
- **Protocol**: The IP protocol (TCP, UDP, ICMP, or All).
- **Ports**: The port or port range allowed.
- **Source**: The source CIDR block or the ID of the source Security Group.

## Technical Details
This tool uses `boto3` to call `ec2:DescribeSecurityGroups`. It flattens the nested `IpPermissions` structure into a linear list of rules, making it much easier to analyze in a spreadsheet or table.

> [!NOTE]
> This tool currently focuses on **Ingress** (inbound) rules, as they represent the primary attack surface.
