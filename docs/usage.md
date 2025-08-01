# Usage Guide

This comprehensive guide covers all features and options available in Rain CLI.

## Command Line Interface

Rain CLI provides a rich command-line interface with various options and flags.

### Basic Syntax

```bash
rain [OPTIONS]
```

### Global Options

#### `-s, --section`
Display specific section(s) only.

```bash
# Single section
rain -s system

# Multiple sections
rain -s system -s hardware -s network

# All sections
rain -s all
```

Available sections:
- `system` - Operating system and basic information
- `hardware` - CPU, memory, disks, GPU, battery
- `network` - Network interfaces, connections, routing
- `processes` - Running processes and resource usage
- `security` - Security status, firewall, open ports
- `sensors` - Temperature and fan sensors
- `python` - Python environment and packages

#### `-l, --live`
Enable live monitoring mode with real-time updates.

```bash
rain --live
```

Features:
- Auto-refreshing display
- Real-time process monitoring
- Live CPU and memory usage
- Press `Ctrl+C` to exit

#### `-j, --json`
Output data in JSON format.

```bash
rain --json
```

Benefits:
- Machine-readable format
- Perfect for automation
- Easy integration with other tools
- Clean, structured data

#### `--save`
Save output to a file.

```bash
# Save as text
rain --save report.txt

# Save as JSON
rain --save data.json --json

# Save specific sections
rain -s system -s hardware --save hardware-report.txt
```

#### `-v, --verbose`
Enable verbose logging for troubleshooting.

```bash
rain -v
```

Shows:
- Detailed collection process
- Error messages and warnings
- Performance information
- Debug information

#### `--config`
Use a custom configuration file.

```bash
rain --config /path/to/config.json
```

#### `--no-banner`
Skip the welcome banner display.

```bash
rain --no-banner
```

Useful for:
- Automation scripts
- Cleaner output
- Integration with other tools

#### `--version`
Show version information.

```bash
rain --version
```

## Section Details

### System Information

```bash
rain -s system
```

Displays:
- Operating system details
- Hostname and FQDN
- Boot time and uptime
- Current users
- System timezone
- Environment variables count

### Hardware Information

```bash
rain -s hardware
```

Displays:
- **CPU**: Brand, cores, frequency, usage
- **Memory**: Virtual and swap memory stats
- **Disks**: Mounted disks with usage and I/O stats
- **GPU**: Graphics cards with memory and usage
- **Battery**: Battery status and health (if available)

### Network Information

```bash
rain -s network
```

Displays:
- **Interfaces**: Network interfaces with IP addresses
- **Connections**: Active network connections
- **Public IP**: External IP address
- **DNS**: DNS servers and search domains
- **Statistics**: Network I/O statistics

### Process Information

```bash
rain -s processes
```

Displays:
- Running processes list
- CPU and memory usage per process
- Process status and creation time
- Process summary statistics
- Top resource consumers

### Security Information

```bash
rain -s security
```

Displays:
- Firewall status
- Open/listening ports
- Admin/sudo privileges
- Security-related system status

### Sensor Information

```bash
rain -s sensors
```

Displays:
- Temperature sensors
- Fan speeds
- Battery information
- Hardware monitoring data

### Python Environment

```bash
rain -s python
```

Displays:
- Python version and implementation
- Virtual environment information
- Installed packages list
- Python executable location
- Site packages information

## Output Formats

### Terminal Display

The default beautiful terminal output with:
- Rich colors and formatting
- Emojis for visual appeal
- Organized tables and panels
- Progress indicators
- Status icons

### JSON Output

Structured JSON data perfect for:

```python
import json
import subprocess

# Get system data as JSON
result = subprocess.run(['rain', '--json', '-s', 'system'], 
                       capture_output=True, text=True)
data = json.loads(result.stdout)

print(f"OS: {data['system']['os']['name']}")
print(f"Uptime: {data['system']['uptime']}")
```

### File Output

Save reports for:
- Documentation
- Audit trails
- Historical comparison
- Sharing with teams

## Live Monitoring

Real-time system monitoring with auto-refresh:

```bash
rain --live
```

Features:
- Updates every few seconds
- Real-time process information
- Live CPU and memory graphs
- Network activity monitoring
- Easy to exit with `Ctrl+C`

Perfect for:
- System monitoring
- Performance troubleshooting
- Resource usage tracking
- Development debugging

## Advanced Usage

### Combining Options

```bash
# Live monitoring with specific sections
rain --live -s hardware -s processes

# JSON output with verbose logging
rain --json -v -s system

# Save live data to file (snapshot)
rain --live --save snapshot.txt

# No banner with specific sections
rain --no-banner -s security -s network
```

### Automation Examples

```bash
# Daily system report
rain --json -s all > daily-report-$(date +%Y%m%d).json

# Monitor specific processes
rain -s processes --no-banner | grep python

# System health check
rain -s system -s hardware --no-banner > health-check.txt
```

### Integration with Scripts

```bash
#!/bin/bash
# System monitoring script

# Get CPU usage as JSON
CPU_DATA=$(rain --json -s hardware --no-banner | jq '.hardware.cpu.usage.percent')

if (( $(echo "$CPU_DATA > 80" | bc -l) )); then
    echo "High CPU usage detected: $CPU_DATA%"
    # Send alert...
fi
```

## Performance Considerations

- **Startup Time**: ~1-2 seconds for full scan
- **Memory Usage**: ~50MB during execution
- **CPU Impact**: Minimal, brief spike during data collection
- **Network Impact**: Only for public IP detection (optional)

## Error Handling

Rain CLI gracefully handles:
- Missing optional dependencies
- Permission denied errors
- Unavailable system features
- Network connectivity issues
- Invalid configuration files

Errors are logged appropriately and don't crash the application.
