# Installation

Rain CLI can be installed in several ways, depending on your preference and use case.

## Prerequisites

Rain CLI requires Python 3.8 or higher. You can check your Python version with:

```bash
python --version
```

## Installation Methods

### Method 1: From PyPI (Recommended)

```bash
pip install rain-cli
```

### Method 2: From Source

1. Clone the repository:
```bash
git clone https://github.com/desenyon/rain.git
cd rain
```

2. Install in development mode:
```bash
pip install -e .
```

### Method 3: Using pipx (Isolated Installation)

If you prefer to install Rain CLI in an isolated environment:

```bash
pipx install rain-cli
```

## Verify Installation

After installation, verify that Rain CLI is working:

```bash
rain --version
```

You should see output similar to:
```
rain, version 1.0.0
```

## Optional Dependencies

Rain CLI works out of the box, but some features require additional dependencies:

### Enhanced Network Information
```bash
pip install netifaces
```

### Detailed CPU Information
```bash
pip install py-cpuinfo
```

### GPU Information (NVIDIA)
```bash
pip install GPUtil
```

### Linux Distribution Information
```bash
pip install distro
```

## System Requirements

- **Python**: 3.8+
- **Operating System**: Linux, macOS, Windows
- **Memory**: Minimal (< 50MB)
- **Disk Space**: < 100MB

## Troubleshooting

### Permission Issues

If you encounter permission errors, you may need to run with elevated privileges:

```bash
# On Linux/macOS
sudo rain

# On Windows (Run as Administrator)
rain
```

### Missing Dependencies

Rain CLI is designed to work gracefully with missing optional dependencies. If a feature is not available, it will be skipped with a warning message.

### Virtual Environments

If you're using a virtual environment, make sure it's activated before installation:

```bash
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

pip install rain-cli
```
