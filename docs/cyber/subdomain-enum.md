# Subdomain Enumerator

The **Subdomain Enumerator** maps a target domain's external attack surface by attempting to resolve common subdomains via DNS queries.

## Syntax

```bash
opsforge cyber subdomain-enum [DOMAIN] [OPTIONS]
```

### Arguments
- `DOMAIN`: The base domain to enumerate (e.g., `google.com`).

### Options
- `-w, --wordlist PATH`: Path to a custom subdomain wordlist.
- `-t, --threads INTEGER`: Number of concurrent threads. [default: 20]
- `--help`: Show this message and exit.

## Usage Examples

### Quick enumeration with defaults
```bash
opsforge cyber subdomain-enum example.com
```

### Enumeration with a large wordlist
```bash
opsforge cyber subdomain-enum target.org -w subdomains_top_5000.txt -t 100
```

## Technical Details
This tool uses a wordlist-based approach (brute-forcing) to identify valid subdomains. It leverages `socket.gethostbyname()` for DNS resolution and `ThreadPoolExecutor` for high-concurrency scanning.

> [!NOTE]
> This tool only performs DNS lookups. It does not interact with the target web servers directly, making it a "passive" discovery tool in terms of HTTP traffic.
