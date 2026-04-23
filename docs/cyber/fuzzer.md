# Vulnerability Fuzzer

The **Vulnerability Fuzzer** is a simple automated tool that injects common attack payloads into URL query parameters to identify potential validation flaws, such as SQL Injection, Cross-Site Scripting (XSS), or Local File Inclusion (LFI).

## Syntax

```bash
opsforge cyber fuzzer [URL] [OPTIONS]
```

### Arguments
- `URL`: The target URL to fuzz (e.g., `http://example.com/search`).

### Options
- `-p, --payloads PATH`: Path to a file containing custom payloads (one per line).
- `--param TEXT`: The query parameter to inject payloads into. [default: id]
- `--help`: Show this message and exit.

## Usage Examples

### Basic fuzzing on the 'id' parameter
```bash
opsforge cyber fuzzer http://scanning.me/profile
```

### Fuzzing a specific 'search' parameter with custom payloads
```bash
opsforge cyber fuzzer http://scanning.me/find -p xss_payloads.txt --param search
```

## How It Works
1. It iterates through a list of payloads (either defaults or from a provided file).
2. It sends an `HTTP GET` request to the target URL for each payload, injecting the payload into the specified query parameter.
3. It records the HTTP status code and response body size.

## Analyzing Results
Look for anomalies in the output table:
- **Status 500 (Internal Server Error)**: Often indicates a crash or unhandled exception on the server, which could be a sign of a vulnerability (especially SQLi).
- **Status 200 with unusual response size**: Significant changes in response size compared to other payloads might indicate that the payload successfully changed the page content (e.g., successful XSS injection or LFI).

## Technical Details
This tool uses the `requests` library to perform HTTP operations. It is designed for basic, deterministic vulnerability probing.

> [!WARNING]
> This tool performs "active" probing and will be logged by the target web server. Use only on systems you own or have explicit permission to test.
