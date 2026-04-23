# Directory Discovery

The **Directory Discovery** tool automates HTTP requests to find hidden web server directories and files by brute-forcing against a wordlist.

## Syntax

```bash
opsforge cyber dir-discover [URL] [OPTIONS]
```

### Arguments
- `URL`: The base URL of the target web server (e.g., `http://example.com`).

### Options
- `-w, --wordlist PATH`: Path to a custom directory wordlist.
- `-t, --threads INTEGER`: Number of concurrent threads. [default: 10]
- `-e, --extensions TEXT`: File extensions to check (comma-separated, e.g., `.php,.html,.bak`).
- `--help`: Show this message and exit.

## Usage Examples

### Quick discovery with defaults
```bash
opsforge cyber dir-discover http://scanning.me
```

### Discovery with custom wordlist and extensions
```bash
opsforge cyber dir-discover 10.0.0.5 -w common_dirs.txt -e .php,.txt,.json -t 50
```

## Technical Details
This tool performs synchronous HTTP requests using the `requests` library. It uses a `ThreadPoolExecutor` to handle multiple requests in parallel. For efficiency, it first sends an `HTTP HEAD` request; if the server responds with a status code other than `404`, it marks the item as found.

> [!NOTE]
> Extensive directory brute-forcing generates significant log noise on the target web server and may be blocked by Web Application Firewalls (WAFs). Use with caution and only on authorized targets.
