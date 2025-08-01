"""
Utility functions for Rain application.
"""

import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple


def run_command(command: List[str], timeout: int = 5) -> Tuple[bool, str, str]:
    """
    Run a command and return success status, stdout, and stderr.
    
    Args:
        command: Command to run as list of strings
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except FileNotFoundError:
        return False, "", "Command not found"
    except Exception as e:
        return False, "", str(e)


def safe_import(module_name: str) -> Optional[Any]:
    """
    Safely import a module and return it, or None if import fails.
    
    Args:
        module_name: Name of module to import
        
    Returns:
        Imported module or None
    """
    try:
        return __import__(module_name)
    except ImportError:
        return None


def get_system_info_fallback() -> Dict[str, Any]:
    """
    Get basic system information using only standard library.
    
    Returns:
        Dictionary with basic system information
    """
    import platform
    import os
    
    return {
        "os": {
            "name": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture(),
            "platform": platform.platform(),
        },
        "python": {
            "version": sys.version,
            "executable": sys.executable,
            "platform": sys.platform,
        },
        "environment_count": len(os.environ),
    }


def format_uptime(seconds: float) -> str:
    """
    Format uptime seconds into human readable format.
    
    Args:
        seconds: Uptime in seconds
        
    Returns:
        Formatted uptime string
    """
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    if not parts:
        return "less than a minute"
    
    return ", ".join(parts)


def check_admin_privileges() -> bool:
    """
    Check if the current user has administrator privileges.
    
    Returns:
        True if user has admin privileges
    """
    import platform
    import os
    
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def get_terminal_size() -> Tuple[int, int]:
    """
    Get terminal size (width, height).
    
    Returns:
        Tuple of (width, height)
    """
    try:
        import shutil
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except Exception:
        return 80, 24  # Default fallback


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to maximum length with suffix.
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= len(suffix):
        return suffix[:max_length]
    
    return text[:max_length - len(suffix)] + suffix


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes into human readable format.
    
    Args:
        bytes_value: Size in bytes
        
    Returns:
        Formatted size string
    """
    if bytes_value == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = abs(bytes_value)
    i = 0
    
    while size >= 1024.0 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {units[i]}"
