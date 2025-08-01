"""
Logging utilities for Rain application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler


def setup_logging(verbose: bool = False, log_file: Optional[Path] = None, suppress_output: bool = False) -> None:
    """
    Setup logging configuration for Rain application.
    
    Args:
        verbose: Enable verbose (DEBUG) logging
        log_file: Optional log file path
        suppress_output: Suppress console output (for JSON mode)
    """
    # Set log level
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler with Rich formatting (unless suppressed)
    if not suppress_output:
        console_handler = RichHandler(
            console=None,  # Use default console
            show_time=False,
            show_path=verbose,
            markup=True,
            rich_tracebacks=True,
        )
        console_handler.setLevel(log_level)
        root_logger.addHandler(console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except OSError as e:
            logging.warning(f"Failed to setup file logging: {e}")
    
    # Set up specific loggers
    rain_logger = logging.getLogger("rain")
    rain_logger.setLevel(log_level)
    
    # Suppress noisy third-party loggers unless in verbose mode
    if not verbose:
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("psutil").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"rain.{name}")
