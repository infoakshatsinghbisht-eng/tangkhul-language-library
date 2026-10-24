# Installation Guide

This guide covers installing the Tangkhul Language Library across different operating systems.

---

## Requirements

- **Python**: `>= 3.10`
- **Pip**: Modern pip recommended (`>= 22.0`)
- **OS**: Windows 10/11, Linux (Ubuntu, Debian, Fedora, Arch), macOS (12+)

---

## Windows PowerShell

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd path\to\tangkhul-language-library
   ```

2. Create a virtual environment:
   ```powershell
   python -m venv .venv
   ```

3. Activate the virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   *(If script execution is disabled, enable it for the current process: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

4. Install the package in editable mode:
   ```powershell
   python -m pip install -e .
   ```

5. Install with development dependencies (pytest, ruff):
   ```powershell
   python -m pip install -e ".[dev]"
   ```

---

## Linux & macOS

1. Open a terminal and navigate to the project directory:
   ```bash
   cd path/to/tangkhul-language-library
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the environment:
   ```bash
   source .venv/bin/activate
   ```

4. Install in editable mode:
   ```bash
   python3 -m pip install -e .
   ```

5. Install development tools:
   ```bash
   python3 -m pip install -e ".[dev]"
   ```

---

## Verification

Verify your installation:

```bash
# Check package version
python -c "import tangkhul_lib; print(tangkhul_lib.__version__)"

# Run CLI info command
tangkhul --info

# Run test suite
python -m pytest

# Run linter
python -m ruff check .
```
