"""
Comprehensive test suite for Rain CLI application.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import psutil
from click.testing import CliRunner

# Add project root to path
import sys
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from cli.main import main
from core.robust_collector import RobustSystemCollector
from core.config import Config
from core.display import DisplayManager
from utils.exceptions import RainError, CollectionError, DisplayError, ConfigError
from utils.logger import setup_logging, get_logger
from utils.helpers import run_command, safe_import, format_uptime, format_bytes


class TestRainCLI(unittest.TestCase):
    """Test the main CLI functionality."""
    
    def setUp(self):
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test that help command works."""
        result = self.runner.invoke(main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Rain - Comprehensive System Information CLI Tool', result.output)
    
    def test_cli_version(self):
        """Test version command."""
        result = self.runner.invoke(main, ['--version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('rain', result.output.lower())
    
    def test_cli_no_banner(self):
        """Test --no-banner flag."""
        result = self.runner.invoke(main, ['--no-banner', '-s', 'system'])
        self.assertEqual(result.exit_code, 0)
        # Should not contain banner elements
        self.assertNotIn('Welcome', result.output)
    
    def test_cli_json_output(self):
        """Test JSON output format."""
        result = self.runner.invoke(main, ['--json', '-s', 'system'])
        self.assertEqual(result.exit_code, 0)
        # Should be valid JSON
        try:
            json.loads(result.output)
        except json.JSONDecodeError:
            self.fail("CLI did not output valid JSON")
    
    def test_cli_save_to_file(self):
        """Test saving output to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            result = self.runner.invoke(main, ['--save', temp_file, '-s', 'system'])
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(temp_file))
            self.assertGreater(os.path.getsize(temp_file), 0)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_cli_specific_sections(self):
        """Test displaying specific sections."""
        result = self.runner.invoke(main, ['-s', 'system', '-s', 'hardware', '--no-banner'])
        self.assertEqual(result.exit_code, 0)
    
    def test_cli_all_sections(self):
        """Test displaying all sections."""
        result = self.runner.invoke(main, ['-s', 'all', '--no-banner'])
        self.assertEqual(result.exit_code, 0)


class TestRobustSystemCollector(unittest.TestCase):
    """Test the system information collector."""
    
    def setUp(self):
        self.config = Config()
        self.collector = RobustSystemCollector(config=self.config)
    
    def test_collector_initialization(self):
        """Test collector initializes correctly."""
        self.assertIsInstance(self.collector, RobustSystemCollector)
        self.assertEqual(self.collector.config, self.config)
    
    def test_collect_system_info(self):
        """Test system information collection."""
        data = self.collector.collect_system_info()
        self.assertIsInstance(data, dict)
        self.assertIn('hostname', data)
        self.assertIn('os', data)
        self.assertIn('uptime', data)
    
    def test_collect_hardware_info(self):
        """Test hardware information collection."""
        data = self.collector.collect_hardware_info()
        self.assertIsInstance(data, dict)
        self.assertIn('cpu', data)
        self.assertIn('memory', data)
        self.assertIn('disks', data)
    
    def test_collect_network_info(self):
        """Test network information collection."""
        data = self.collector.collect_network_info()
        self.assertIsInstance(data, dict)
        self.assertIn('interfaces', data)
        self.assertIn('connections', data)
    
    def test_collect_process_info(self):
        """Test process information collection."""
        data = self.collector.collect_process_info()
        self.assertIsInstance(data, dict)
        self.assertIn('processes', data)
        self.assertIn('count', data)
    
    def test_collect_all_data(self):
        """Test collecting all data for specific sections."""
        sections = ['system', 'hardware']
        data = self.collector.collect_all_data(sections)
        self.assertIsInstance(data, dict)
        self.assertIn('system', data)
        self.assertIn('hardware', data)
        self.assertNotIn('network', data)  # Not requested
    
    def test_collect_all_data_all_sections(self):
        """Test collecting all data for all sections."""
        sections = ['system', 'hardware', 'network', 'processes', 'security', 'sensors', 'python']
        data = self.collector.collect_all_data(sections)
        self.assertIsInstance(data, dict)
        for section in sections:
            self.assertIn(section, data)
    
    @patch('psutil.cpu_percent')
    def test_cpu_usage_collection(self, mock_cpu):
        """Test CPU usage collection with mocking."""
        mock_cpu.return_value = 50.0
        data = self.collector.collect_hardware_info()
        self.assertIn('cpu', data)
        mock_cpu.assert_called()
    
    @patch('psutil.virtual_memory')
    def test_memory_collection(self, mock_memory):
        """Test memory collection with mocking."""
        mock_memory.return_value = Mock(
            total=8589934592,  # 8GB
            available=4294967296,  # 4GB
            percent=50.0,
            used=4294967296
        )
        data = self.collector.collect_hardware_info()
        self.assertIn('memory', data)
        mock_memory.assert_called()


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        self.assertIsInstance(config.default_sections, list)
        self.assertIsInstance(config.live_update_interval, float)
        self.assertIsInstance(config.enable_colors, bool)
    
    def test_config_from_dict(self):
        """Test loading configuration from dictionary."""
        config_dict = {
            'default_sections': ['system'],
            'live_update_interval': 1.0,
            'enable_colors': False
        }
        config = Config.from_dict(config_dict)
        self.assertEqual(config.default_sections, ['system'])
        self.assertEqual(config.live_update_interval, 1.0)
        self.assertFalse(config.enable_colors)
    
    def test_config_to_dict(self):
        """Test converting configuration to dictionary."""
        config = Config()
        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertIn('default_sections', config_dict)
        self.assertIn('live_update_interval', config_dict)
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = Config()
        config.validate()  # Should not raise exception
        
        # Test invalid temperature unit
        config.temperature_unit = "invalid"
        with self.assertRaises(ConfigError):
            config.validate()


class TestDisplayManager(unittest.TestCase):
    """Test display management functionality."""
    
    def setUp(self):
        from rich.console import Console
        self.config = Config()
        self.console = Console(file=open(os.devnull, 'w'))  # Suppress output
        self.display = DisplayManager(config=self.config, console=self.console)
    
    def tearDown(self):
        self.console.file.close()
    
    def test_display_manager_initialization(self):
        """Test display manager initializes correctly."""
        self.assertIsInstance(self.display, DisplayManager)
        self.assertEqual(self.display.config, self.config)
    
    def test_format_bytes(self):
        """Test byte formatting utility."""
        self.assertEqual(self.display._format_bytes(1024), "1.0 KB")
        self.assertEqual(self.display._format_bytes(1048576), "1.0 MB")
        self.assertEqual(self.display._format_bytes(1073741824), "1.0 GB")
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        self.assertEqual(self.display._format_percentage(50.0), "50.0%")
        self.assertEqual(self.display._format_percentage(100.0), "100.0%")
    
    def test_display_system_info(self):
        """Test system info display."""
        mock_data = {
            'hostname': 'test-host',
            'platform': 'Linux',
            'uptime': '1 day, 2 hours'
        }
        # Should not raise exception
        self.display._display_system_info(mock_data)
    
    def test_output_json(self):
        """Test JSON output functionality."""
        mock_data = {'system': {'hostname': 'test'}}
        # Should not raise exception when outputting to console
        self.display.output_json(mock_data)
    
    def test_save_to_file(self):
        """Test saving data to file."""
        mock_data = {'system': {'hostname': 'test'}}
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            self.display.save_to_file(mock_data, temp_file, ['system'])
            self.assertTrue(os.path.exists(temp_file))
            self.assertGreater(os.path.getsize(temp_file), 0)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestUtilities(unittest.TestCase):
    """Test utility functions."""
    
    def test_format_bytes(self):
        """Test byte formatting utility."""
        from utils.helpers import format_bytes
        self.assertEqual(format_bytes(1024), "1.0 KB")
        self.assertEqual(format_bytes(1048576), "1.0 MB")
        self.assertEqual(format_bytes(1073741824), "1.0 GB")
        self.assertEqual(format_bytes(0), "0 B")
    
    def test_format_uptime(self):
        """Test uptime formatting."""
        from utils.helpers import format_uptime
        # Test with seconds (less than a minute)
        self.assertEqual(format_uptime(30), "less than a minute")
        # Test with minutes
        self.assertIn("minute", format_uptime(90))
        # Test with hours  
        self.assertIn("hour", format_uptime(3700))
    
    def test_safe_import(self):
        """Test safe import functionality."""
        from utils.helpers import safe_import
        
        # Test importing existing module
        os_module = safe_import("os")
        self.assertIsNotNone(os_module)
        
        # Test importing non-existent module
        fake_module = safe_import("this_module_does_not_exist")
        self.assertIsNone(fake_module)
    
    def test_run_command(self):
        """Test command execution utility."""
        from utils.helpers import run_command
        
        # Test successful command
        success, stdout, stderr = run_command(["echo", "test"])
        self.assertTrue(success)
        self.assertIn("test", stdout)
        
        # Test command with error
        success, stdout, stderr = run_command(["false"])  # Command that returns non-zero exit code
        self.assertFalse(success)
    
    def test_logging_setup(self):
        """Test logging setup."""
        # Test basic setup
        setup_logging(verbose=False)
        logger = get_logger("test")
        self.assertIsNotNone(logger)
        
        # Test verbose setup
        setup_logging(verbose=True)
        verbose_logger = get_logger("test_verbose")
        self.assertIsNotNone(verbose_logger)


class TestExceptions(unittest.TestCase):
    """Test custom exceptions."""
    
    def test_rain_error(self):
        """Test base RainError exception."""
        with self.assertRaises(RainError):
            raise RainError("Test error")
    
    def test_collection_error(self):
        """Test CollectionError exception."""
        with self.assertRaises(CollectionError):
            raise CollectionError("Collection failed")
    
    def test_display_error(self):
        """Test DisplayError exception."""
        with self.assertRaises(DisplayError):
            raise DisplayError("Display failed")
    
    def test_config_error(self):
        """Test ConfigError exception."""
        with self.assertRaises(ConfigError):
            raise ConfigError("Config invalid")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete application."""
    
    def setUp(self):
        self.runner = CliRunner()
    
    def test_end_to_end_system_section(self):
        """Test complete workflow for system section."""
        result = self.runner.invoke(main, ['-s', 'system', '--no-banner'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('SYSTEM INFORMATION', result.output)
    
    def test_end_to_end_json_output(self):
        """Test complete workflow with JSON output."""
        result = self.runner.invoke(main, ['--json', '-s', 'system'])
        self.assertEqual(result.exit_code, 0)
        
        # Verify it's valid JSON
        try:
            data = json.loads(result.output)
            self.assertIsInstance(data, dict)
            self.assertIn('system', data)
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
    
    def test_end_to_end_file_output(self):
        """Test complete workflow with file output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
        
        try:
            result = self.runner.invoke(main, ['--save', temp_file, '-s', 'system', '--no-banner'])
            self.assertEqual(result.exit_code, 0)
            
            # Verify file was created and has content
            self.assertTrue(os.path.exists(temp_file))
            with open(temp_file, 'r') as f:
                content = f.read()
                self.assertGreater(len(content), 0)
                self.assertIn('SYSTEM INFORMATION', content)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test invalid section
        result = self.runner.invoke(main, ['-s', 'invalid_section'])
        self.assertNotEqual(result.exit_code, 0)
    
    @patch('core.robust_collector.RobustSystemCollector.collect_all_data')
    def test_collection_error_handling(self, mock_collect):
        """Test handling of collection errors."""
        mock_collect.side_effect = CollectionError("Mock collection error")
        result = self.runner.invoke(main, ['-s', 'system', '--no-banner'])
        self.assertNotEqual(result.exit_code, 0)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
