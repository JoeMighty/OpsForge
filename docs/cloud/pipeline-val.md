# CI Pipeline Validator

The **CI Pipeline Validator** parses YAML configuration files for popular CI/CD platforms (GitHub Actions, GitLab CI) to ensure they adhere to organizational testing standards and security best practices.

## Syntax

```bash
opsforge cloud pipeline-val [FILE]
```

### Arguments
- `FILE`: Path to the CI YAML file (e.g., `.github/workflows/deploy.yml`).

## Usage Examples

### Validate a GitHub Actions workflow
```bash
opsforge cloud pipeline-val .github/workflows/main.yml
```

### Validate a GitLab CI file
```bash
opsforge cloud pipeline-val .gitlab-ci.yml
```

## Standards Audited

### Platform Detection
Automatically identifies if the file is a GitHub Actions workflow or a GitLab CI configuration based on the top-level keys (`jobs` vs `stages`).

### Automated Testing Check
Verifies that the pipeline contains at least one job or stage dedicated to testing (checks for keywords like `test` or `check`).

### Secret Security
Performs a heuristic scan of `run` commands to identify potential hardcoded secrets (passwords, tokens). It flags commands that contain sensitive keywords but do not use the platform's native secret injection syntax (e.g., `${{ secrets.VAR }}`).

## Technical Details
This tool uses `PyYAML` for deterministic parsing of the configuration files and applies a set of rule-based heuristics to the resulting data structure.

> [!WARNING]
> This linter provides a "baseline" check. It is not a replacement for comprehensive security tools like **Checkov** or **Gitleaks**, but rather a quick way to ensure developers haven't bypassed basic testing requirements.
