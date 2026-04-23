# Infra Boilerplate Generator

The **Infra Boilerplate Generator** outputs standardized, best-practice infrastructure-as-code templates (Terraform). It uses Jinja2 templating to inject project-specific variables into a consistent base architecture.

## Syntax

```bash
opsforge cloud infra-gen [OPTIONS]
```

### Options
- `-t, --type [terraform]`: Type of infrastructure code to generate. [default: terraform]
- `-p, --project TEXT`: Project name (used for resource naming). [default: opsforge-project]
- `-r, --region TEXT`: Target AWS region. [default: us-east-1]
- `--vpc-cidr TEXT`: CIDR block for the VPC. [default: 10.0.0.0/16]
- `-o, --output PATH`: Output filename. [default: main.tf]
- `--help`: Show this message and exit.

## Usage Examples

### Generate a standard Terraform baseline
```bash
opsforge cloud infra-gen -p my-app -r eu-central-1
```

## Generated Resources
The default Terraform template includes:
- **VPC**: A VPC with the specified CIDR block and project tags.
- **S3 Bucket**: A private data bucket with `force_destroy` enabled.
- **S3 Public Access Block**: Strict blocking of all public access to the S3 bucket to ensure security by default.

## Technical Details
This tool uses **Jinja2** to render `.j2` templates stored within the package. The logic is entirely local and deterministic, ensuring that the same inputs always result in the same boilerplate code.

> [!TIP]
> Use this tool to quickly initialize new cloud projects with security-first defaults (like private S3 buckets) instead of starting from scratch.
