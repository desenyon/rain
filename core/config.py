"""
Configuration management for Rain application.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.exceptions import ConfigError


@dataclass
class Config:
    """Configuration class for Rain application."""
    
    # Default sections to display
    default_sections: List[str] = field(default_factory=lambda: ["system", "hardware", "network"])
    
    # Live update settings
    live_update_interval: float = 2.0
    enable_live_updates: bool = True
    
    # Display settings
    enable_colors: bool = True
    page_size: int = 50
    temperature_unit: str = "celsius"  # celsius or fahrenheit
    
    # Network settings
    network_timeout: int = 5
    dns_servers: List[str] = field(default_factory=lambda: ["8.8.8.8", "1.1.1.1"])
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Performance settings
    max_processes: int = 1000
    enable_caching: bool = True
    cache_duration: int = 60  # seconds
    
    # Config file path
    _config_file: Optional[Path] = field(default=None, init=False)
    
    def __post_init__(self):
        """Initialize configuration after dataclass creation."""
        # This will be called with config_path when needed
        pass
    
    @classmethod
    def create(cls, config_path: Optional[str] = None) -> "Config":
        """Create a Config instance and load from file."""
        config = cls()
        config._config_file = config._get_config_file_path(config_path)
        config._load_config()
        return config
    
    def _get_config_file_path(self, custom_path: Optional[str] = None) -> Path:
        """Get the configuration file path."""
        if custom_path:
            return Path(custom_path)
        
        # Default config locations
        config_dir = Path.home() / ".rain"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if not self._config_file or not self._config_file.exists():
            return
        
        try:
            with open(self._config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # Update attributes with loaded values
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
        except (json.JSONDecodeError, OSError) as e:
            raise ConfigError(f"Failed to load config file {self._config_file}: {e}")
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        if not self._config_file:
            return
            
        # Ensure directory exists
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            "default_sections": self.default_sections,
            "live_update_interval": self.live_update_interval,
            "enable_colors": self.enable_colors,
            "temperature_unit": self.temperature_unit,
            "network_timeout": self.network_timeout,
            "log_level": self.log_level,
            "max_processes": self.max_processes,
            "enable_caching": self.enable_caching,
            "cache_duration": self.cache_duration,
        }
        
        try:
            with open(str(self._config_file), 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)
        except OSError as e:
            raise ConfigError(f"Failed to save config file {self._config_file}: {e}")
    
    def get_log_file_path(self) -> Optional[Path]:
        """Get the log file path if logging to file is enabled."""
        if self.log_file:
            return Path(self.log_file)
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "default_sections": self.default_sections,
            "live_update_interval": self.live_update_interval,
            "enable_colors": self.enable_colors,
            "temperature_unit": self.temperature_unit,
            "network_timeout": self.network_timeout,
            "log_level": self.log_level,
            "max_processes": self.max_processes,
            "enable_caching": self.enable_caching,
            "cache_duration": self.cache_duration,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create Config instance from dictionary."""
        config = cls()
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config
    
    def validate(self) -> None:
        """Validate configuration values."""
        if self.temperature_unit not in ["celsius", "fahrenheit"]:
            raise ConfigError(f"Invalid temperature unit: {self.temperature_unit}")
        
        if self.live_update_interval <= 0:
            raise ConfigError("Live update interval must be positive")
        
        if self.network_timeout <= 0:
            raise ConfigError("Network timeout must be positive")
        
        if self.max_processes <= 0:
            raise ConfigError("Max processes must be positive")
        
        if self.cache_duration <= 0:
            raise ConfigError("Cache duration must be positive")
