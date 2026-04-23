# Network Port Scanner

The **Network Port Scanner** probes IP addresses for open ports using raw socket connections. It is a high-speed, multi-threaded utility designed for rapid surface mapping.

## Syntax

```bash
opsforge cyber port-scan [TARGET] [OPTIONS]
```

### Arguments
- `TARGET`: The IP address or hostname to scan.

### Options
- `-p, --ports TEXT`: Port range (e.g., `80,443` or `1-1024`). [default: 1-1024]
- `-t, --threads INTEGER`: Number of concurrent threads. [default: 50]
- `--timeout FLOAT`: Socket timeout in seconds. [default: 1.0]
- `--help`: Show this message and exit.

## Usage Examples

### Scan common ports
```bash
opsforge cyber port-scan 192.168.1.1
```

### Scan specific ports
```bash
opsforge cyber port-scan 10.0.0.5 -p 22,80,443,3306
```

### Scan a large range with high concurrency
```bash
opsforge cyber port-scan scanning.me -p 1-65535 -t 200
```

## Technical Details
This tool uses Python's native `socket` library to attempt TCP connections. It uses a `ThreadPoolExecutor` to handle multiple connection attempts simultaneously without blocking the main thread.

> [!NOTE]
> This tool performs a "Full Connect" scan, which is detectable by most Intrusion Detection Systems (IDS).
