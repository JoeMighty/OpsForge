# Uptime Health Monitor

The **Uptime Health Monitor** pings cloud endpoints (URLs) at regular intervals to verify their availability. It alerts the user immediately if any endpoint returns a non-200 status code or becomes unreachable.

## Syntax

```bash
opsforge cloud uptime-monitor [URLS...] [OPTIONS]
```

### Arguments
- `URLS`: One or more URLs to monitor (space-separated).

### Options
- `-i, --interval INTEGER`: Interval between checks in seconds. [default: 60]
- `-c, --count INTEGER`: Number of checks to perform (0 for infinite). [default: 1]
- `--help`: Show this message and exit.

## Usage Examples

### Single check of multiple endpoints
```bash
opsforge cloud uptime-monitor api.myapp.com auth.myapp.com
```

### Continuous monitoring every 30 seconds
```bash
opsforge cloud uptime-monitor https://status.myapp.com -i 30 -c 0
```

## How It Works
The tool uses the `requests` library to send `HTTP GET` requests to each provided URL.
- **Success**: Status code `200 OK`.
- **Warning/Critical**: Any other status code (e.g., `404`, `500`, `503`).
- **Down**: Connection timeout or resolution failure.

## Metrics Recorded
- **Status Code**: The HTTP response code from the server.
- **Latency**: The time taken (in milliseconds) to receive the response.
- **Timestamp**: The exact time the check was performed.

## Technical Details
This tool runs in a simple loop on the main thread. It is designed for lightweight, manual monitoring or for use in background terminal sessions.

> [!TIP]
> For production environments, always complement this tool with managed services like **AWS Route53 Health Checks** or **CloudWatch Synthetics**.
