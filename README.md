<div align="center">

# 🛠️ OpsForge

**A consolidated toolkit for cybersecurity professionals and cloud infrastructure architects.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=plastic)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg?style=plastic)](https://www.python.org/)
[![CLI: Click](https://img.shields.io/badge/CLI-Click-teal.svg?style=plastic)](https://click.palletsprojects.com/)
[![Documentation: MkDocs](https://img.shields.io/badge/Docs-MkDocs-cyan.svg?style=plastic)](https://www.mkdocs.org/)
[![Status: Development](https://img.shields.io/badge/Status-Development-orange.svg?style=plastic)]()

[Installation](#installation) • [Documentation Hub](#documentation-hub) • [Tool Overview](#tool-overview) • [Contributing](#contributing)

---

</div>

## 🚀 Overview

**OpsForge** is a monolithic Command Line Interface (CLI) application that wraps 22 individual utilities into a unified command structure. Built for speed, determinism, and reliability, it eliminates the need for fragmented scripts and provides a professional, high-end terminal experience.

### Key Features
- **Zero AI Dependency**: All tools run deterministic logic for predictable results.
- **Offline Capable**: Core tools (Entropy checkers, encoders, etc.) function without external APIs.
- **Unified Interface**: One command (`opsforge`) to access every tool in the suite.
- **Rich Output**: Beautifully formatted tables, progress bars, and status updates using `rich`.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/JoeMighty/OpsForge.git

# Navigate to the project
cd OpsForge

# Install the package in editable mode
pip install -e .
```

## 📚 Documentation Hub

The full documentation, including detailed command references and technical guides, is available via GitHub Pages (built with MkDocs Material).

> [!TIP]
> Visit the documentation at: **[https://joemighty.github.io/OpsForge/](https://joemighty.github.io/OpsForge/)**

## 🛠️ Tool Overview

### 🛡️ Cybersecurity (Cyber)
| Tool | Description |
| :--- | :--- |
| `port-scan` | Multi-threaded TCP port probing. |
| `log-analyze` | Forensic analysis of server access logs. |
| `integrity-check` | Cryptographic file auditing. |
| `subdomain-enum` | DNS-based attack surface mapping. |
| `password-check` | Mathematical entropy evaluation. |
| ... and 6 more. | [View all Cyber tools](docs/cyber/index.md) |

### ☁️ Cloud Infrastructure (Cloud)
| Tool | Description |
| :--- | :--- |
| `tag-audit` | AWS resource compliance auditor. |
| `iam-lint` | IAM policy permissive rule detector. |
| `infra-gen` | Terraform boilerplate generation. |
| `stale-find` | Idle/Unattached resource identifier. |
| `storage-audit` | S3 public exposure checker. |
| ... and 6 more. | [View all Cloud tools](docs/cloud/index.md) |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details on how to add new tools or improve existing ones.

---

<div align="center">
Built with ❤️ by the OpsForge Team
</div>
