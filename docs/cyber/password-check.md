# Password Entropy Checker

The **Password Entropy Checker** evaluates the mathematical strength of passwords offline. It calculates the Shannon entropy to estimate how many bits of information the password contains.

## Syntax

```bash
opsforge cyber password-check [PASSWORD] [OPTIONS]
```

### Arguments
- `PASSWORD`: The password string to evaluate (optional if using interactive mode).

### Options
- `-i, --interactive`: Prompt for the password securely (prevents the password from appearing in shell history).
- `--help`: Show this message and exit.

## Usage Examples

### Quick check
```bash
opsforge cyber password-check "P@ssw0rd123!"
```

### Secure interactive check (Recommended)
```bash
opsforge cyber password-check -i
```

## Understanding Entropy
Entropy is measured in bits. It represents the number of guesses required to crack a password in a worst-case brute-force scenario ($2^E$ guesses).

| Entropy | Strength |
| --- | --- |
| < 40 bits | Very Weak |
| 40-60 bits | Weak |
| 60-80 bits | Moderate |
| 80-100 bits | Strong |
| > 100 bits | Very Strong |

## Technical Details
This tool uses the formula $E = L \times \log_2(R)$, where:
- $L$ is the length of the password.
- $R$ is the size of the character pool (charset) used in the password.

It automatically detects the charset size based on the presence of lowercase, uppercase, digits, and special characters.

> [!IMPORTANT]
> This tool runs entirely **offline**. Your password is never sent to any server or API.
