# Changelog

All notable changes to Rain CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documentation with Read the Docs support
- Comprehensive API documentation
- Examples and usage guides

## [1.0.0] - 2025-08-01

### Added
- Initial release of Rain CLI
- Beautiful terminal interface with Rich library
- Comprehensive system information collection
- Support for multiple output formats (terminal, JSON, file)
- Live monitoring mode with real-time updates
- Cross-platform support (Linux, macOS, Windows)
- Configurable sections and display options
- Robust error handling and graceful fallbacks
- Complete test suite with 40+ tests

#### System Information Features
- Operating system details and version information
- Hostname, FQDN, boot time, and uptime
- Current logged-in users
- Environment variables and system timezone
- Linux distribution information (when available)

#### Hardware Information Features
- CPU information (brand, cores, frequency, usage)
- Memory statistics (virtual and swap memory)
- Disk information with usage and I/O statistics
- GPU information (NVIDIA support via nvidia-smi)
- Battery status and health information
- Hardware sensor readings (temperature, fans)

#### Network Information Features
- Network interface details with IP addresses
- Active network connections
- Public IP address detection
- DNS server configuration
- Network I/O statistics
- Routing information and default gateway

#### Process Information Features
- Running process list with detailed statistics
- CPU and memory usage per process
- Process status and creation time
- Process summary and categorization
- Configurable process limits and filtering

#### Security Information Features
- Firewall status detection
- Open/listening ports enumeration
- Administrative privilege checking
- Security-related system status

#### Python Environment Features
- Python version and implementation details
- Virtual environment detection
- Installed packages enumeration
- Python executable location
- Site packages information

#### CLI Features
- Multiple section selection (`-s system -s hardware`)
- Live monitoring mode (`--live`)
- JSON output format (`--json`)
- File output with automatic format detection (`--save`)
- Verbose logging (`-v`)
- Custom configuration file support (`--config`)
- Banner control (`--no-banner`)
- Version information (`--version`)

#### Display Features
- Rich terminal formatting with colors and emojis
- Organized tables and panels for data presentation
- Progress indicators and status displays
- Beautiful ASCII art banner
- Responsive layout and formatting
- Cross-platform terminal compatibility

#### Configuration Features
- JSON-based configuration files
- Environment variable support
- Configurable default sections
- Display customization options
- Performance tuning parameters
- Filter and threshold settings

#### Error Handling
- Custom exception hierarchy
- Graceful handling of missing dependencies
- Permission error recovery
- Network timeout handling
- Invalid configuration validation

#### Testing
- Comprehensive test suite with 40+ test cases
- Unit tests for all major components
- Integration tests for end-to-end workflows
- Mock testing for external dependencies
- Cross-platform testing considerations

### Dependencies
- `psutil` - System and process information
- `requests` - HTTP requests for public IP detection
- `rich` - Beautiful terminal formatting
- `click` - Command-line interface framework

### Optional Dependencies
- `netifaces` - Enhanced network interface information
- `py-cpuinfo` - Detailed CPU information
- `GPUtil` - NVIDIA GPU information
- `distro` - Linux distribution information

### Technical Details
- Python 3.8+ compatibility
- Cross-platform architecture with fallbacks
- Modular design with separation of concerns
- Efficient data collection with smart caching
- Memory-efficient processing
- Robust error handling patterns

### Performance
- Fast startup time (~1-2 seconds)
- Low memory footprint (~50MB)
- Efficient data collection algorithms
- Minimal CPU impact during operation
- Smart caching for repeated operations

[unreleased]: https://github.com/desenyon/rain/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/desenyon/rain/releases/tag/v1.0.0
