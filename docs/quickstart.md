# Quick Start

Get up and running with Rain CLI in just a few minutes!

## Basic Usage

### Show All Information

The simplest way to use Rain CLI is to run it without any arguments:

```bash
rain
```

This will display all available system information in a beautiful, formatted output.

### Show Specific Sections

You can display specific sections using the `-s` or `--section` flag:

```bash
# Show only system information
rain -s system

# Show system and hardware information
rain -s system -s hardware

# Show all sections explicitly
rain -s all
```

Available sections:
- `system` - OS, hostname, uptime, users
- `hardware` - CPU, memory, disks, GPU, battery
- `network` - Network interfaces, connections, public IP
- `processes` - Running processes and their stats
- `security` - Firewall, open ports, privileges
- `sensors` - Temperature and fan sensors
- `python` - Python environment and packages

## Output Formats

### Terminal Display (Default)

Beautiful, colorful terminal output with emojis and tables:

```bash
rain
```

### JSON Output

Perfect for automation and integration:

```bash
rain --json
```

### Save to File

Save the output to a file for later analysis:

```bash
# Save as text
rain --save system-report.txt

# Save as JSON
rain --save system-report.json --json
```

## Live Monitoring

Monitor your system in real-time:

```bash
rain --live
```

Press `Ctrl+C` to exit live monitoring mode.

## Common Examples

### System Administrator Tasks

```bash
# Quick system overview
rain -s system -s hardware

# Check running processes
rain -s processes

# Monitor system in real-time
rain --live

# Generate JSON report for monitoring tools
rain --json > /var/log/system-info.json
```

### Developer Tasks

```bash
# Check Python environment
rain -s python

# Get system specs for bug reports
rain -s system -s hardware --save bug-report.txt

# Monitor resource usage during development
rain --live -s hardware -s processes
```

### Security Auditing

```bash
# Check security status
rain -s security

# List all network connections
rain -s network

# Get comprehensive security report
rain -s security -s network -s processes --save security-audit.json --json
```

## Configuration

### Skip the Banner

If you prefer cleaner output:

```bash
rain --no-banner
```

### Verbose Logging

For troubleshooting:

```bash
rain -v
```

### Custom Configuration

Create a configuration file for your preferred settings:

```bash
rain --config /path/to/config.json
```

## Next Steps

- Learn about [detailed usage](usage.md) options
- Explore [configuration](configuration.md) possibilities
- Check out more [examples](examples.md)
- Read the [API documentation](api/index.md)
