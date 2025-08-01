# Configuration API

```{eval-rst}
.. automodule:: core.config
   :members:
   :undoc-members:
   :show-inheritance:
```

## Config

Configuration management for Rain CLI.

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
