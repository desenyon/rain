# Configuration

Rain CLI can be customized through configuration files to match your preferences and requirements.

## Configuration File

Rain CLI uses JSON configuration files to customize behavior, display options, and data collection settings.

### Default Configuration

Rain CLI works perfectly without any configuration, but you can create a configuration file to customize its behavior.

### Configuration File Location

You can specify a configuration file using the `--config` option:

```bash
rain --config /path/to/config.json
```

Or place a configuration file in one of these default locations:
- `~/.rain/config.json` (user-specific)
- `~/.config/rain/config.json` (XDG config directory)
- `/etc/rain/config.json` (system-wide, Linux/macOS)

## Configuration Options

### Basic Configuration

```json
{
  "default_sections": ["system", "hardware"],
  "show_banner": true,
  "refresh_interval": 2,
  "max_processes": 50,
  "network_timeout": 5
}
```

### Complete Configuration Example

```json
{
  "default_sections": [
    "system",
    "hardware",
    "network",
    "processes"
  ],
  "display": {
    "show_banner": true,
    "theme": "default",
    "colors": true,
    "emojis": true,
    "table_style": "rounded"
  },
  "collection": {
    "max_processes": 100,
    "network_timeout": 10,
    "include_environment": false,
    "detailed_cpu_info": true,
    "collect_gpu_info": true
  },
  "live_mode": {
    "refresh_interval": 2,
    "auto_scroll": true,
    "highlight_changes": true
  },
  "output": {
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "number_format": "human",
    "json_indent": 2
  },
  "filters": {
    "exclude_processes": ["kernel_task", "launchd"],
    "min_cpu_threshold": 0.1,
    "min_memory_threshold": 10
  }
}
```

## Configuration Sections

### Default Sections

```json
{
  "default_sections": ["system", "hardware", "network"]
}
```

Specifies which sections to display by default when no `-s` option is provided.

Available sections:
- `system` - Basic system information
- `hardware` - Hardware details
- `network` - Network information
- `processes` - Process information
- `security` - Security status
- `sensors` - Sensor data
- `python` - Python environment

### Display Settings

```json
{
  "display": {
    "show_banner": true,
    "theme": "default",
    "colors": true,
    "emojis": true,
    "table_style": "rounded"
  }
}
```

- **show_banner**: Show/hide the welcome banner
- **theme**: Color theme (default, dark, light)
- **colors**: Enable/disable colored output
- **emojis**: Enable/disable emoji icons
- **table_style**: Table border style (rounded, simple, heavy)

### Collection Settings

```json
{
  "collection": {
    "max_processes": 100,
    "network_timeout": 10,
    "include_environment": false,
    "detailed_cpu_info": true,
    "collect_gpu_info": true
  }
}
```

- **max_processes**: Maximum number of processes to display
- **network_timeout**: Timeout for network operations (seconds)
- **include_environment**: Include environment variables in system info
- **detailed_cpu_info**: Collect detailed CPU information (requires py-cpuinfo)
- **collect_gpu_info**: Attempt to collect GPU information

### Live Mode Settings

```json
{
  "live_mode": {
    "refresh_interval": 2,
    "auto_scroll": true,
    "highlight_changes": true
  }
}
```

- **refresh_interval**: Update interval in seconds
- **auto_scroll**: Auto-scroll to show latest data
- **highlight_changes**: Highlight changed values

### Output Settings

```json
{
  "output": {
    "timestamp_format": "%Y-%m-%d %H:%M:%S",
    "number_format": "human",
    "json_indent": 2
  }
}
```

- **timestamp_format**: Python strftime format for timestamps
- **number_format**: Number formatting (human, raw)
- **json_indent**: JSON output indentation

### Filters

```json
{
  "filters": {
    "exclude_processes": ["kernel_task", "launchd"],
    "min_cpu_threshold": 0.1,
    "min_memory_threshold": 10
  }
}
```

- **exclude_processes**: Process names to exclude from display
- **min_cpu_threshold**: Minimum CPU usage to display (percentage)
- **min_memory_threshold**: Minimum memory usage to display (MB)

## Environment Variables

You can also configure Rain CLI using environment variables:

```bash
# Set default sections
export RAIN_DEFAULT_SECTIONS="system,hardware"

# Disable banner
export RAIN_SHOW_BANNER=false

# Set refresh interval
export RAIN_REFRESH_INTERVAL=5

# Set maximum processes
export RAIN_MAX_PROCESSES=50

# Set network timeout
export RAIN_NETWORK_TIMEOUT=10
```

Environment variables override configuration file settings.

## Configuration Examples

### Minimal Configuration

For basic usage with clean output:

```json
{
  "default_sections": ["system"],
  "display": {
    "show_banner": false,
    "emojis": false
  }
}
```

### Performance Monitoring

For system monitoring and performance analysis:

```json
{
  "default_sections": ["hardware", "processes"],
  "collection": {
    "max_processes": 200,
    "detailed_cpu_info": true
  },
  "live_mode": {
    "refresh_interval": 1,
    "highlight_changes": true
  },
  "filters": {
    "min_cpu_threshold": 1.0,
    "min_memory_threshold": 50
  }
}
```

### Security Auditing

For security assessment and auditing:

```json
{
  "default_sections": ["system", "network", "security", "processes"],
  "collection": {
    "max_processes": 500,
    "network_timeout": 15
  },
  "display": {
    "show_banner": false
  },
  "output": {
    "timestamp_format": "%Y-%m-%d %H:%M:%S UTC"
  }
}
```

### Automation/Scripting

For automated monitoring and scripting:

```json
{
  "default_sections": ["all"],
  "display": {
    "show_banner": false,
    "colors": false,
    "emojis": false
  },
  "collection": {
    "include_environment": true,
    "detailed_cpu_info": true,
    "collect_gpu_info": true
  }
}
```

## Validation

Rain CLI validates configuration files and will show helpful error messages for:
- Invalid JSON syntax
- Unknown configuration keys
- Invalid values
- Type mismatches

Example validation error:
```
Error: Invalid configuration value for 'refresh_interval': must be a number between 1 and 60
```

## Configuration Priority

Settings are applied in this order (highest to lowest priority):
1. Command line arguments
2. Environment variables
3. Configuration file (--config)
4. Default configuration file
5. Built-in defaults

This allows for flexible configuration while maintaining sensible defaults.
