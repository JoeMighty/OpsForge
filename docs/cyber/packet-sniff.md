# Packet Sniffer Utility

The **Packet Sniffer Utility** captures and decodes local network traffic headers and payloads in real-time. It is built on the powerful `scapy` library.

## Syntax

```bash
opsforge cyber packet-sniff [OPTIONS]
```

### Options
- `-i, --iface TEXT`: Interface to sniff on (e.g., `eth0`, `wlan0`, `en0`).
- `-c, --count INTEGER`: Number of packets to capture. [default: 10]
- `-f, --filter TEXT`: BPF (Berkeley Packet Filter) string (e.g., `'tcp and port 80'`).
- `--help`: Show this message and exit.

## Usage Examples

### Capture 10 packets on default interface
```bash
opsforge cyber packet-sniff
```

### Capture HTTP traffic on a specific interface
```bash
opsforge cyber packet-sniff -i eth0 -f "tcp port 80" -c 50
```

### Capture only UDP traffic
```bash
opsforge cyber packet-sniff -f "udp"
```

## Technical Details
This tool uses **Scapy** to interface with the network stack. It decodes standard IP, TCP, and UDP headers and attempts to display the raw payload data (in hex format) if available.

> [!WARNING]
> **Privileged Access Required**: This tool typically requires administrative or root privileges to access the network interface in promiscuous mode. On Windows, ensure you are running the terminal as Administrator. On Linux/macOS, use `sudo`.

## BPF Filter Cheat Sheet
- `tcp`: Capture only TCP packets.
- `udp`: Capture only UDP packets.
- `port 80`: Capture traffic to/from port 80.
- `host 1.1.1.1`: Capture traffic to/from a specific IP.
- `net 192.168.1.0/24`: Capture traffic for an entire subnet.
