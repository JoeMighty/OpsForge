# File Integrity Monitor

The **File Integrity Monitor (FIM)** calculates and compares cryptographic hashes (SHA-256) of local system files to detect unauthorized changes, deletions, or new file additions.

## Syntax

```bash
opsforge cyber integrity-check [COMMAND] [ARGS]
```

### Commands

#### `generate`
Creates a fingerprint (JSON file) containing hashes of all files in a directory.

```bash
opsforge cyber integrity-check generate [DIRECTORY] [OPTIONS]
```
- `DIRECTORY`: Path to the directory to fingerprint.
- `-o, --output TEXT`: Output filename. [default: fingerprint.json]

#### `verify`
Compares a directory against an existing fingerprint file.

```bash
opsforge cyber integrity-check verify [DIRECTORY] [FINGERPRINT_FILE]
```
- `DIRECTORY`: Path to the directory to verify.
- `FINGERPRINT_FILE`: Path to the JSON fingerprint file.

## Usage Examples

### Baseline a system directory
```bash
opsforge cyber integrity-check generate /etc/nginx -o nginx_baseline.json
```

### Verify integrity later
```bash
opsforge cyber integrity-check verify /etc/nginx nginx_baseline.json
```

## Detection Capabilities
- **MODIFIED**: Files whose content has changed (different SHA-256 hash).
- **MISSING**: Files that were in the baseline but are now gone.
- **NEW**: Files that exist in the directory but were not in the baseline.

## Technical Details
This tool implements the **SHA-256** algorithm via Python's `hashlib`. It reads files in 4096-byte blocks to ensure memory efficiency even when hashing large files.

> [!WARNING]
> Ensure the baseline fingerprint file is stored in a secure, read-only location or on a separate system to prevent attackers from tampering with the baseline itself.
