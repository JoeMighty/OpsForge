# SSL Certificate Auditor

The **SSL Certificate Auditor** retrieves and analyzes SSL/TLS certificates for a given hostname. It checks expiration dates, issuer authenticity, and the strength of the cryptographic protocols and ciphers in use.

## Syntax

```bash
opsforge cyber ssl-audit [HOSTNAME] [OPTIONS]
```

### Arguments
- `HOSTNAME`: The domain or IP to audit (e.g., `google.com`).

### Options
- `-p, --port INTEGER`: Port to check. [default: 443]
- `--help`: Show this message and exit.

## Usage Examples

### Audit a standard web server
```bash
opsforge cyber ssl-audit google.com
```

### Audit a custom port
```bash
opsforge cyber ssl-audit local-dev.server -p 8443
```

## Metrics Audited
- **Status**: Whether the certificate is currently valid or expired.
- **Expiration**: The exact date/time the certificate expires and the remaining days.
- **Protocol**: The TLS version in use (e.g., `TLSv1.3`).
- **Cipher**: The encryption algorithm negotiated for the connection.
- **Issuer**: The Certificate Authority (CA) that signed the certificate.

## Technical Details
This tool uses Python's native `ssl` and `socket` modules. It performs a standard TLS handshake to retrieve the server's public certificate and connection metadata. It does not require external binary dependencies like OpenSSL to be installed on the system path.

> [!TIP]
> Always ensure your servers support **TLSv1.2** or **TLSv1.3** and disable older, insecure protocols like SSLv3 or TLSv1.0.
