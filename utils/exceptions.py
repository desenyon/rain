"""
Custom exceptions for Rain application.
"""


class RainError(Exception):
    """Base exception for Rain application."""
    pass


class ConfigError(RainError):
    """Configuration related errors."""
    pass


class CollectionError(RainError):
    """Data collection related errors."""
    pass


class DisplayError(RainError):
    """Display related errors."""
    pass


class NetworkError(RainError):
    """Network related errors."""
    pass


class PermissionError(RainError):
    """Permission related errors."""
    pass
