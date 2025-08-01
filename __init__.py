"""
Rain - Comprehensive System Information CLI Tool

A Python CLI application that displays extensive system information
in a beautiful, interactive terminal interface.
"""

__version__ = "1.0.0"
__author__ = "desenyon"
__email__ = "desenyon@gmail.com"
__license__ = "MIT"

from core.collector import SystemCollector
from core.display import DisplayManager
from core.config import Config

__all__ = ["SystemCollector", "DisplayManager", "Config"]
