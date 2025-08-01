# Exceptions API

```{eval-rst}
.. automodule:: utils.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
```

## Exception Hierarchy

Rain CLI uses a hierarchy of custom exceptions for proper error handling.

```
RainError
├── ConfigError
├── CollectionError
└── DisplayError
```

## RainError

Base exception class for all Rain CLI errors.

**Usage:**
```python
from utils.exceptions import RainError

try:
    # Rain CLI operation
    pass
except RainError as e:
    print(f"Rain error: {e}")
```

## ConfigError

Raised when configuration errors occur.

**Common Causes:**
- Invalid configuration file format
- Missing required configuration values
- Invalid configuration value types

**Example:**
```python
from utils.exceptions import ConfigError

try:
    config = Config.create(config_path='invalid.json')
except ConfigError as e:
    print(f"Configuration error: {e}")
```

## CollectionError

Raised when system information collection fails.

**Common Causes:**
- Permission denied for system information
- Missing system features or files
- External command failures

**Example:**
```python
from utils.exceptions import CollectionError
from core.robust_collector import RobustSystemCollector

try:
    collector = RobustSystemCollector()
    data = collector.collect_system_info()
except CollectionError as e:
    print(f"Collection failed: {e}")
```

## DisplayError

Raised when display or output operations fail.

**Common Causes:**
- Invalid display data format
- File write permissions
- Terminal compatibility issues

**Example:**
```python
from utils.exceptions import DisplayError
from core.display import DisplayManager

try:
    display = DisplayManager()
    display.save_to_file(data, '/readonly/file.txt', sections)
except DisplayError as e:
    print(f"Display error: {e}")
```

## Error Handling Best Practices

### Catch Specific Exceptions

```python
from utils.exceptions import RainError, CollectionError, DisplayError

try:
    # Rain CLI operations
    pass
except CollectionError as e:
    # Handle collection-specific errors
    logger.error(f"Failed to collect data: {e}")
except DisplayError as e:
    # Handle display-specific errors
    logger.error(f"Failed to display data: {e}")
except RainError as e:
    # Handle any other Rain errors
    logger.error(f"Rain error: {e}")
```

### Graceful Degradation

```python
from utils.exceptions import CollectionError

def collect_with_fallback():
    try:
        return collector.collect_detailed_info()
    except CollectionError:
        logger.warning("Detailed collection failed, using basic info")
        return collector.collect_basic_info()
```

### User-Friendly Error Messages

```python
from utils.exceptions import ConfigError

try:
    config = Config.create(config_path=user_config)
except ConfigError as e:
    print(f"Configuration error: {e}")
    print("Please check your configuration file and try again.")
    sys.exit(1)
```
