# System Collector API

The `RobustSystemCollector` class provides comprehensive system information collection with graceful fallbacks for missing dependencies.

## RobustSystemCollector

The main class for collecting system information with graceful fallbacks.

### Class Definition

```python
class RobustSystemCollector:
    """A robust system collector that handles missing dependencies."""
    
    def __init__(self, config=None):
        """Initialize the collector with optional configuration."""
```

### Methods

#### collect_all_data(sections)
Collect information for specified sections.

**Parameters:**
- `sections` (List[str]): List of section names to collect

**Returns:**
- `Dict[str, Any]`: Dictionary containing collected data

**Example:**
```python
from core.robust_collector import RobustSystemCollector

collector = RobustSystemCollector()
data = collector.collect_all_data(['system', 'hardware'])
```

#### collect_system_info()
Collect basic system information.

**Returns:**
- `Dict[str, Any]`: System information including OS, hostname, uptime, users

#### collect_hardware_info()
Collect hardware information.

**Returns:**
- `Dict[str, Any]`: Hardware information including CPU, memory, disks, GPU, battery

#### collect_network_info()
Collect network information.

**Returns:**
- `Dict[str, Any]`: Network information including interfaces, connections, public IP

#### collect_process_info()
Collect process information.

**Returns:**
- `Dict[str, Any]`: Process information including running processes and statistics

#### collect_security_info()
Collect security information.

**Returns:**
- `Dict[str, Any]`: Security information including firewall, open ports, privileges

#### collect_sensor_info()
Collect sensor information.

**Returns:**
- `Dict[str, Any]`: Sensor information including temperature and fan readings

#### collect_python_info()
Collect Python environment information.

**Returns:**
- `Dict[str, Any]`: Python information including version, packages, environment
