# API Documentation

Rain CLI provides a comprehensive Python API for programmatic access to system information.

```{toctree}
:maxdepth: 2

collector
display
config
exceptions
```

## Overview

The Rain CLI API is organized into several main modules:

- **Collector** - System information collection
- **Display** - Output formatting and display
- **Config** - Configuration management
- **Exceptions** - Error handling

## Quick Start

### Basic Usage

```python
from core.robust_collector import RobustSystemCollector
from core.display import DisplayManager
from core.config import Config

# Initialize with default config
config = Config()
collector = RobustSystemCollector(config=config)

# Collect system information
data = collector.collect_system_info()
print(f"OS: {data['os']['name']}")
print(f"Uptime: {data['uptime']}")
```

### Collecting Specific Sections

```python
# Collect specific sections
sections = ['system', 'hardware', 'network']
all_data = collector.collect_all_data(sections)

# Access specific data
cpu_info = all_data['hardware']['cpu']
print(f"CPU: {cpu_info['brand']}")
print(f"Cores: {cpu_info['cores']['logical']}")
```

### Display Management

```python
from rich.console import Console

console = Console()
display = DisplayManager(config=config, console=console)

# Display formatted output
display.display_all(all_data, sections)

# Output as JSON
display.output_json(all_data)

# Save to file
display.save_to_file(all_data, 'report.json', sections)
```

## Core Classes

### RobustSystemCollector

The main class for collecting system information with graceful fallbacks.

```python
collector = RobustSystemCollector(config=config)

# Collect all data
data = collector.collect_all_data(['system', 'hardware'])

# Collect specific sections
system_info = collector.collect_system_info()
hardware_info = collector.collect_hardware_info()
network_info = collector.collect_network_info()
```

### DisplayManager

Handles output formatting and display in various formats.

```python
display = DisplayManager(config=config, console=console)

# Terminal display
display.display_all(data, sections)

# JSON output
display.output_json(data)

# File output
display.save_to_file(data, 'output.txt', sections)

# Live monitoring
display.run_live_monitor(collector, sections)
```

### Config

Configuration management for customizing behavior.

```python
# Default configuration
config = Config()

# Load from file
config = Config.create(config_path='config.json')

# Access settings
print(config.default_sections)
print(config.max_processes)
```

## Error Handling

Rain CLI uses custom exceptions for proper error handling:

```python
from utils.exceptions import RainError, CollectionError, DisplayError

try:
    data = collector.collect_system_info()
except CollectionError as e:
    print(f"Failed to collect data: {e}")
except RainError as e:
    print(f"Rain error: {e}")
```

## Data Structures

### System Information

```python
{
    "os": {
        "name": "Darwin",
        "release": "21.0.0",
        "version": "Darwin Kernel Version...",
        "machine": "arm64",
        "processor": "arm",
        "architecture": ["64bit", "Mach-O"],
        "platform": "macOS-12.0-arm64-arm-64bit"
    },
    "hostname": "example.local",
    "fqdn": "example.local",
    "boot_time": "2023-01-01T00:00:00",
    "uptime": "1 day, 2 hours, 30 minutes",
    "uptime_seconds": 95400,
    "current_time": "2023-01-02T02:30:00",
    "timezone": "('EST', 'EDT')",
    "users": [
        {
            "name": "user",
            "terminal": "console",
            "host": "local",
            "started": "2023-01-01T08:00:00"
        }
    ]
}
```

### Hardware Information

```python
{
    "cpu": {
        "brand": "Apple M1",
        "cores": {
            "physical": 8,
            "logical": 8
        },
        "frequency": {
            "current": 2400.0,
            "min": 600.0,
            "max": 3200.0
        },
        "usage": {
            "percent": 15.2,
            "per_core": [10.0, 20.0, 15.0, 12.0]
        }
    },
    "memory": {
        "virtual": {
            "total": 17179869184,
            "available": 12884901888,
            "used": 4294967296,
            "free": 8589934592,
            "percent": 25.0
        },
        "swap": {
            "total": 2147483648,
            "used": 0,
            "free": 2147483648,
            "percent": 0.0
        }
    }
}
```

## Integration Examples

### Monitoring Script

```python
#!/usr/bin/env python3
import time
from core.robust_collector import RobustSystemCollector
from core.config import Config

def monitor_system():
    config = Config()
    collector = RobustSystemCollector(config=config)
    
    while True:
        try:
            data = collector.collect_hardware_info()
            cpu_usage = data['cpu']['usage']['percent']
            memory_usage = data['memory']['virtual']['percent']
            
            print(f"CPU: {cpu_usage:.1f}% | Memory: {memory_usage:.1f}%")
            
            if cpu_usage > 80:
                print("⚠️  High CPU usage detected!")
            
            if memory_usage > 85:
                print("⚠️  High memory usage detected!")
                
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    monitor_system()
```

### Data Export

```python
import json
from datetime import datetime
from core.robust_collector import RobustSystemCollector
from core.config import Config

def export_system_data():
    config = Config()
    collector = RobustSystemCollector(config=config)
    
    # Collect all available data
    sections = ['system', 'hardware', 'network', 'processes']
    data = collector.collect_all_data(sections)
    
    # Add metadata
    report = {
        'timestamp': datetime.now().isoformat(),
        'rain_version': '1.0.0',
        'sections': sections,
        'data': data
    }
    
    # Save to file
    filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"System data exported to {filename}")

if __name__ == "__main__":
    export_system_data()
```

### Custom Display

```python
from rich.console import Console
from rich.table import Table
from core.robust_collector import RobustSystemCollector
from core.config import Config

def custom_cpu_display():
    config = Config()
    collector = RobustSystemCollector(config=config)
    console = Console()
    
    # Get CPU data
    hardware_data = collector.collect_hardware_info()
    cpu_data = hardware_data['cpu']
    
    # Create custom table
    table = Table(title="CPU Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Brand", cpu_data['brand'])
    table.add_row("Physical Cores", str(cpu_data['cores']['physical']))
    table.add_row("Logical Cores", str(cpu_data['cores']['logical']))
    table.add_row("Usage", f"{cpu_data['usage']['percent']:.1f}%")
    
    console.print(table)

if __name__ == "__main__":
    custom_cpu_display()
```
