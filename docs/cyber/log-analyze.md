# Access Log Analyzer

The **Access Log Analyzer** parses server logs (Apache/Nginx) to flag repeated failed logins, traffic spikes, and potential web attacks like SQL Injection or XSS.

## Syntax

```bash
opsforge cyber log-analyze [LOGFILE] [OPTIONS]
```

### Arguments
- `LOGFILE`: Path to the server log file (e.g., `access.log`).

### Options
- `--threshold INTEGER`: Threshold for flagging IPs (failed logins or request count). [default: 10]
- `--help`: Show this message and exit.

## Usage Examples

### Standard analysis
```bash
opsforge cyber log-analyze /var/log/nginx/access.log
```

### Analysis with lower threshold
```bash
opsforge cyber log-analyze access.log --threshold 5
```

## Detected Patterns

### High Traffic
Identifies IPs making an unusually high number of requests within the log file. This can help identify scraping bots or potential DoS attempts.

### Failed Logins
Scans for `401` (Unauthorized) and `403` (Forbidden) status codes associated with specific IPs. Multiple failures from a single IP often indicate a brute-force attempt.

### Web Attacks
Uses regex patterns to find common attack strings in URL fragments:
- **SQL Injection**: `SELECT`, `UNION`, `INSERT`, etc.
- **XSS**: `<script>`, `alert(`, etc.

## Technical Details
The tool uses Python's `re` (Regular Expression) module to parse log lines according to the **Combined Log Format**. It uses `collections.Counter` for efficient frequency tracking.

> [!TIP]
> Run this tool periodically via a cron job and pipe the output to a file or alert system for continuous monitoring.
