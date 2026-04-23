# Payload Encoder/Decoder

The **Payload Encoder/Decoder** converts strings between common formats used in web applications and security testing: Base64, Hex, and URL encoding.

## Syntax

```bash
opsforge cyber encode-decode [TYPE] [DATA] [OPTIONS]
```

### Types
- `base64`: Base64 encoding/decoding.
- `hex`: Hexadecimal encoding/decoding.
- `url`: URL (percent) encoding/decoding.

### Options
- `-d, --decode`: Perform decoding instead of encoding.
- `--help`: Show this message and exit.

## Usage Examples

### Base64 encode a string
```bash
opsforge cyber encode-decode base64 "secret_payload"
```

### Base64 decode a string
```bash
opsforge cyber encode-decode base64 "c2VjcmV0X3BheWxvYWQ=" -d
```

### URL encode a string
```bash
opsforge cyber encode-decode url "admin' OR 1=1 --"
```

### Hex encode a string
```bash
opsforge cyber encode-decode hex "Hello World"
```

## Technical Details
This tool uses Python's standard libraries (`base64`, `urllib.parse`, and built-in `hex` methods) to ensure deterministic and accurate transformations.

> [!TIP]
> Use URL encoding when crafting payloads for web forms or URL parameters to ensure special characters are handled correctly by the server.
