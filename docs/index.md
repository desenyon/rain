# Rain CLI Documentation

Welcome to Rain CLI, a comprehensive system information tool that displays every piece of knowable information about your computer in a beautiful, interactive terminal interface.

```{toctree}
:maxdepth: 2
:caption: Contents:

installation
quickstart
usage
configuration
api/index
examples
contributing
changelog
```

## What is Rain CLI?

🌧️ **Rain CLI** is a powerful command-line tool that provides comprehensive system information in a beautiful, easy-to-read format. Whether you're a system administrator, developer, or just curious about your system, Rain CLI gives you detailed insights into:

- **System Information** - OS details, hostname, uptime, users
- **Hardware Information** - CPU, memory, disks, GPU, battery
- **Network Information** - Interfaces, connections, public IP, DNS
- **Process Information** - Running processes with detailed stats
- **Security Information** - Firewall status, open ports, privileges
- **Sensor Information** - Temperature, fans, battery status
- **Python Environment** - Version, packages, virtual environments

## Key Features

✨ **Beautiful Terminal Output** - Rich, colorful display with emojis and tables
🔄 **Live Monitoring** - Real-time system monitoring with auto-refresh
📄 **Multiple Output Formats** - Terminal display, JSON, and file output
⚙️ **Configurable** - Customizable sections and display options
🛡️ **Robust** - Graceful handling of missing dependencies and permissions
🚀 **Fast** - Efficient data collection with smart caching
🌍 **Cross-Platform** - Works on Linux, macOS, and Windows

## Quick Example

```bash
# Show all system information
rain

# Show specific sections
rain -s system -s hardware

# Live monitoring mode
rain --live

# Output as JSON
rain --json

# Save to file
rain --save report.txt
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
