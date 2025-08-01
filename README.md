# 🌧️ Rain - Comprehensive System Information CLI Tool

A Python CLI application that displays extensive system information in a beautiful, interactive terminal interface.

## ✨ Features

* **System Info** : Shows your operating system, computer name, uptime, and system type
* **Hardware Info** : Displays CPU, RAM, disk, GPU, and battery details, including real-time usage
* **Network Info** : Lists network interfaces, current connections, IP addresses, and checks if you're online
* **Running Processes** : Shows all active programs and how much CPU and memory they use
* **Security Info** : Shows firewall status, open ports, and basic security settings
* **Sensors** : Displays temperature, fan speeds, and power usage
* **Python Environment** : Shows your Python version, installed packages, and virtual environment info
* **Live Monitoring** : Updates system stats in real time with auto-refresh
* **Export Options** : Allows saving info to files like JSON

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/desenyon/rain.git
   cd rain
   ```
2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Usage

**Basic usage - display all information:**

```bash
python rain.py
```

**Display specific sections:**

```bash
python rain.py -s system -s hardware
```

**Live monitoring mode:**

```bash
python rain.py --live
```

**Export to JSON:**

```bash
python rain.py --json
```

**Save to file:**

```bash
python rain.py --save report.txt
```

**Help and options:**

```bash
python rain.py --help
```

## 📋 Available Sections

- `system` - Operating system and basic information
- `hardware` - CPU, memory, disk, GPU, and battery
- `network` - Network interfaces, connections, and statistics
- `processes` - Running processes and system activity
- `security` - Security settings and firewall status
- `sensors` - Temperature, fan, and power sensors
- `python` - Python environment and installed packages
- `all` - All available sections

## 🎯 Command Line Options

| Option            | Description                      |
| ----------------- | -------------------------------- |
| `-s, --section` | Display specific section(s) only |
| `-l, --live`    | Enable live monitoring mode      |
| `-j, --json`    | Output in JSON format            |
| `--save FILE`   | Save output to file              |
| `-v, --verbose` | Enable verbose logging           |
| `--config FILE` | Use custom configuration file    |
| `--no-banner`   | Skip the banner display          |
| `--version`     | Show version information         |
| `--help`        | Show help message                |

## 🔧 Configuration

Rain can be configured through environment variables or a configuration file:

### Environment Variables

- `RAIN_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)
- `RAIN_CACHE_DURATION`: Cache duration in seconds
- `RAIN_NETWORK_TIMEOUT`: Network operation timeout

### Configuration File

Create a JSON configuration file:

```json
{
    "default_sections": ["system", "hardware", "network"],
    "live_update_interval": 2.0,
    "enable_colors": true,
    "temperature_unit": "celsius",
    "network_timeout": 5,
    "log_level": "INFO"
}
```

Use with `--config config.json`

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests.py
```

# 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
