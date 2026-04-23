# Local Honeypot Listener

The **Local Honeypot Listener** opens deceptive local services on specified ports. It logs every connection attempt, including the source IP and timestamp, providing an early warning system for internal network scanning or unauthorized access attempts.

## Syntax

```bash
opsforge cyber honeypot [OPTIONS]
```

### Options
- `-p, --ports TEXT`: Comma-separated list of ports to listen on. [default: 21,22,23,80,443,3306]
- `-o, --output PATH`: Log file to store connection alerts. [default: honeypot.log]
- `--help`: Show this message and exit.

## Usage Examples

### Start with default ports
```bash
opsforge cyber honeypot
```

### Listen on custom sensitive ports
```bash
opsforge cyber honeypot -p 1433,1521,3389,5900 -o intrusions.log
```

## How It Works
The tool initializes TCP listeners on all specified ports using multiple threads. When a connection is established:
1. It logs the source IP and timestamp.
2. It displays a real-time "ALARM" in the console.
3. It sends a generic service banner (e.g., a fake SSH or FTP header) to entice the scanner/attacker into revealing more information.
4. It immediately closes the connection.

## Technical Details
This utility uses Python's `socket` module for raw networking and `threading` to manage simultaneous listeners across different ports. It is designed to be lightweight and purely deterministic.

> [!IMPORTANT]
> **Port Conflicts**: This tool cannot listen on ports that are already in use by legitimate services on your machine.
> **Privileges**: Listening on well-known ports (below 1024) typically requires administrator/root privileges.
