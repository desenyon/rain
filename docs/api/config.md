# Configuration API

The `Config` class provides configuration management for Rain CLI.

## Config

Configuration management for Rain CLI.

### Class Definition

```python
@dataclass
class Config:
    """Configuration class for Rain CLI with default values."""
    
    default_sections: List[str] = field(default_factory=lambda: ["system", "hardware"])
    max_processes: int = 100
    refresh_interval: float = 2.0
    network_timeout: int = 5
    show_banner: bool = True
```

### Class Methods

#### create(config_path=None)
Create a configuration instance.

**Parameters:**
- `config_path` (Optional[str]): Path to configuration file

**Returns:**
- `Config`: Configuration instance

### Properties

#### default_sections
List of default sections to display.

**Type:** `List[str]`

#### max_processes
Maximum number of processes to display.

**Type:** `int`

#### refresh_interval
Refresh interval for live mode (seconds).

**Type:** `float`

#### network_timeout
Network operation timeout (seconds).

**Type:** `int`

#### show_banner
Whether to show the welcome banner.

**Type:** `bool`

### Methods

#### load_from_file(file_path)
Load configuration from file.

**Parameters:**
- `file_path` (str): Path to configuration file

#### to_dict()
Convert configuration to dictionary.

**Returns:**
- `Dict[str, Any]`: Configuration as dictionary

#### validate()
Validate configuration values.

**Raises:**
- `ConfigError`: If configuration is invalid

### Configuration Schema

```json
{
  "default_sections": ["system", "hardware"],
  "max_processes": 100,
  "refresh_interval": 2.0,
  "network_timeout": 5,
  "show_banner": true,
  "display": {
    "colors": true,
    "emojis": true,
    "table_style": "rounded"
  }
}
```
