# Contributing to OpsForge

We welcome contributions to OpsForge! Whether you're fixing a bug, improving documentation, or adding a completely new utility, your help is appreciated.

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/OpsForge.git
    cd OpsForge
    ```
3.  **Install in editable mode** with development dependencies:
    ```bash
    pip install -e .
    ```

## Adding a New Tool

### 1. Create the Module
Add a new Python file in `opsforge/modules/cyber/` or `opsforge/modules/cloud/`. Use the existing tools as a template, utilizing `click` for the CLI and `rich` for output.

### 2. Register the Command
Update `opsforge/main.py` to import your module and add it to the appropriate command group (`cyber` or `cloud`).

### 3. Add Documentation
Create a corresponding Markdown file in `docs/cyber/` or `docs/cloud/`. Link it in the `mkdocs.yml` navigation section.

## Style Guidelines
- Use **Type Hints** for all function signatures.
- Follow **PEP 8** for Python code style.
- Ensure all output uses the `opsforge.core.output` utilities for consistency.
- Keep tools **deterministic** and avoid AI dependencies.

## Testing
Please add unit tests for your changes in the `tests/` directory and ensure they pass before submitting a Pull Request.

```bash
pytest
```

---

Thank you for helping make OpsForge better!
