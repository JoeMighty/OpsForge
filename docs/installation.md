# Installation

OpsForge is a Python-based CLI application. Follow these steps to install it on your system.

## Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **Git**

## Standard Installation

You can install OpsForge directly from the repository:

```bash
git clone https://github.com/JoeMighty/OpsForge.git
cd OpsForge
pip install -e .
```

The `-e` flag installs the package in "editable" mode, which is recommended if you plan to update the tools frequently.

## Verification

Once installed, verify the installation by running:

```bash
opsforge --version
```

You should see output similar to: `opsforge, version 0.1.0`.

## Dependencies

OpsForge relies on several powerful libraries:
- `click`: CLI framework.
- `rich`: Beautiful terminal formatting.
- `scapy`: Packet manipulation.
- `boto3`: AWS SDK.
- `pyyaml`: YAML parsing for config and pipelines.
