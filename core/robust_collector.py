"""
Robust system information collector with graceful fallbacks.
"""

import json
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import psutil
import requests

from utils.exceptions import CollectionError
from utils.logger import get_logger
from utils.helpers import run_command, safe_import, format_uptime

logger = get_logger("collector")

# Optional imports with fallbacks
distro = safe_import("distro")
netifaces = safe_import("netifaces")


class RobustSystemCollector:
    """A robust system collector that handles missing dependencies."""
    
    def __init__(self, config=None):
        """Initialize the collector."""
        self.config = config
        self._cache = {}
        self._cache_timestamps = {}
    
    def collect_all_data(self, sections: List[str]) -> Dict[str, Any]:
        """Collect all requested system information."""
        data = {}
        
        section_collectors = {
            "system": self.collect_system_info,
            "hardware": self.collect_hardware_info,
            "network": self.collect_network_info,
            "processes": self.collect_process_info,
            "security": self.collect_security_info,
            "sensors": self.collect_sensor_info,
            "python": self.collect_python_info,
        }
        
        for section in sections:
            if section in section_collectors:
                try:
                    logger.info(f"Collecting {section} information")
                    data[section] = section_collectors[section]()
                except Exception as e:
                    logger.error(f"Failed to collect {section} information: {e}")
                    data[section] = {"error": str(e)}
        
        return data
    
    def collect_system_info(self) -> Dict[str, Any]:
        """Collect basic system information."""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime_seconds = time.time() - psutil.boot_time()
            
            system_info = {
                "os": {
                    "name": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                    "architecture": platform.architecture(),
                    "platform": platform.platform(),
                },
                "hostname": socket.gethostname(),
                "fqdn": socket.getfqdn(),
                "boot_time": boot_time.isoformat(),
                "uptime": format_uptime(uptime_seconds),
                "uptime_seconds": uptime_seconds,
                "current_time": datetime.now().isoformat(),
                "timezone": str(time.tzname),
                "users": self._get_users(),
                "environment_count": len(os.environ),
            }
            
            # Add Linux distribution info if available
            if platform.system() == "Linux" and distro:
                try:
                    system_info["os"]["distribution"] = {
                        "name": distro.name(),
                        "version": distro.version(),
                        "codename": distro.codename(),
                        "id": distro.id(),
                    }
                except Exception:
                    pass
            
            return system_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect system information: {e}")
    
    def _get_users(self) -> List[Dict[str, Any]]:
        """Get current users safely."""
        try:
            return [
                {
                    "name": user.name,
                    "terminal": user.terminal or "N/A",
                    "host": user.host or "local",
                    "started": datetime.fromtimestamp(user.started).isoformat()
                }
                for user in psutil.users()
            ]
        except Exception:
            return []
    
    def collect_hardware_info(self) -> Dict[str, Any]:
        """Collect hardware information."""
        try:
            hardware_info = {
                "cpu": self._get_cpu_info(),
                "memory": self._get_memory_info(),
                "disks": self._get_disk_info(),
                "gpu": self._get_gpu_info(),
                "battery": self._get_battery_info(),
            }
            
            return hardware_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect hardware information: {e}")
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information with fallbacks."""
        cpu_info = {
            "brand": platform.processor() or "Unknown",
            "architecture": platform.machine() or "Unknown",
            "cores": {
                "physical": psutil.cpu_count(logical=False) or 1,
                "logical": psutil.cpu_count(logical=True) or 1,
            },
            "usage": {
                "percent": 0,
                "per_core": [],
            },
        }
        
        # Get CPU usage safely
        try:
            cpu_info["usage"]["percent"] = psutil.cpu_percent(interval=0.1)
            cpu_info["usage"]["per_core"] = psutil.cpu_percent(interval=0.1, percpu=True)
        except Exception:
            pass
        
        # Get CPU frequency safely
        try:
            freq = psutil.cpu_freq()
            if freq:
                cpu_info["frequency"] = {
                    "current": freq.current,
                    "min": freq.min,
                    "max": freq.max,
                }
        except Exception:
            pass
        
        # Try to get more detailed CPU info
        cpuinfo = safe_import("cpuinfo")
        if cpuinfo:
            try:
                cpu_data = cpuinfo.get_cpu_info()
                cpu_info.update({
                    "brand": cpu_data.get("brand_raw", cpu_info["brand"]),
                    "model": cpu_data.get("model_name", "Unknown"),
                    "vendor_id": cpu_data.get("vendor_id", "Unknown"),
                })
            except Exception:
                pass
        
        return cpu_info
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "virtual": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "percent": memory.percent,
                    "active": getattr(memory, 'active', None),
                    "inactive": getattr(memory, 'inactive', None),
                    "buffers": getattr(memory, 'buffers', None),
                    "cached": getattr(memory, 'cached', None),
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent,
                }
            }
        except Exception:
            return {"virtual": {}, "swap": {}}
    
    def _get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk information."""
        disks = []
        
        try:
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    disk_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": (usage.used / usage.total) * 100 if usage.total > 0 else 0,
                    }
                    
                    disks.append(disk_info)
                    
                except (PermissionError, OSError):
                    continue
        except Exception:
            pass
        
        return disks
    
    def _get_gpu_info(self) -> List[Dict[str, Any]]:
        """Get GPU information with multiple fallbacks."""
        gpus = []
        
        # Try GPUtil first
        GPUtil = safe_import("GPUtil")
        if GPUtil:
            try:
                gpu_list = GPUtil.getGPUs()
                for gpu in gpu_list:
                    gpu_info = {
                        "id": gpu.id,
                        "name": gpu.name,
                        "memory": {
                            "total": gpu.memoryTotal,
                            "used": gpu.memoryUsed,
                            "free": gpu.memoryFree,
                            "percent": gpu.memoryUtil * 100,
                        },
                        "temperature": gpu.temperature,
                        "load": gpu.load * 100,
                    }
                    gpus.append(gpu_info)
                return gpus
            except Exception:
                pass
        
        # Try nvidia-smi
        success, stdout, _ = run_command([
            "nvidia-smi", 
            "--query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu",
            "--format=csv,noheader,nounits"
        ])
        
        if success:
            for line in stdout.strip().split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 5:
                        try:
                            gpus.append({
                                "name": parts[0],
                                "memory": {
                                    "total": int(parts[1]) if parts[1].isdigit() else 0,
                                    "used": int(parts[2]) if parts[2].isdigit() else 0,
                                },
                                "temperature": int(parts[3]) if parts[3].isdigit() else None,
                                "load": int(parts[4]) if parts[4].isdigit() else None,
                            })
                        except ValueError:
                            continue
        
        return gpus
    
    def _get_battery_info(self) -> Optional[Dict[str, Any]]:
        """Get battery information."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                time_left = "Unlimited"
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                    time_left = format_uptime(battery.secsleft)
                
                return {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "time_left": time_left,
                }
        except Exception:
            pass
        
        return None
    
    def collect_network_info(self) -> Dict[str, Any]:
        """Collect network information."""
        try:
            network_info = {
                "interfaces": self._get_network_interfaces(),
                "connections": self._get_network_connections(),
                "public_ip": self._get_public_ip(),
                "dns": self._get_dns_info(),
                "statistics": self._get_network_statistics(),
            }
            
            return network_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect network information: {e}")
    
    def _get_network_interfaces(self) -> List[Dict[str, Any]]:
        """Get network interfaces with fallback."""
        interfaces = []
        
        if netifaces:
            try:
                for interface_name in netifaces.interfaces():
                    interface_info = {
                        "name": interface_name,
                        "addresses": {},
                        "stats": None,
                    }
                    
                    # Get addresses
                    addresses = netifaces.ifaddresses(interface_name)
                    for family, addrs in addresses.items():
                        family_name = {
                            netifaces.AF_INET: "ipv4",
                            netifaces.AF_INET6: "ipv6",
                            netifaces.AF_LINK: "mac",
                        }.get(family, f"family_{family}")
                        
                        interface_info["addresses"][family_name] = addrs
                    
                    # Get stats
                    try:
                        stats = psutil.net_io_counters(pernic=True).get(interface_name)
                        if stats:
                            interface_info["stats"] = stats._asdict()
                    except Exception:
                        pass
                    
                    interfaces.append(interface_info)
                    
            except Exception:
                pass
        
        # Fallback: use psutil only
        if not interfaces:
            try:
                stats = psutil.net_io_counters(pernic=True)
                for interface_name, stat in stats.items():
                    interfaces.append({
                        "name": interface_name,
                        "addresses": {},
                        "stats": stat._asdict(),
                    })
            except Exception:
                pass
        
        return interfaces
    
    def _get_network_connections(self) -> List[Dict[str, Any]]:
        """Get network connections."""
        connections = []
        
        try:
            for conn in psutil.net_connections(kind='inet'):
                connection_info = {
                    "type": str(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status,
                    "pid": conn.pid,
                }
                
                # Get process name
                if conn.pid:
                    try:
                        process = psutil.Process(conn.pid)
                        connection_info["process_name"] = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        connection_info["process_name"] = "Unknown"
                
                connections.append(connection_info)
                
        except psutil.AccessDenied:
            logger.warning("Access denied when collecting network connections")
        except Exception:
            pass
        
        return connections
    
    def _get_public_ip(self) -> Optional[str]:
        """Get public IP address."""
        try:
            response = requests.get(
                "https://api.ipify.org",
                timeout=self.config.network_timeout if self.config else 5
            )
            if response.status_code == 200:
                return response.text.strip()
        except Exception:
            pass
        
        return None
    
    def _get_dns_info(self) -> Dict[str, Any]:
        """Get DNS information."""
        dns_info = {"servers": [], "search_domains": []}
        
        # Try to read resolv.conf on Unix
        if platform.system() != "Windows":
            try:
                resolv_conf = Path("/etc/resolv.conf")
                if resolv_conf.exists():
                    with open(resolv_conf, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("nameserver"):
                                parts = line.split()
                                if len(parts) > 1:
                                    dns_info["servers"].append(parts[1])
                            elif line.startswith("search"):
                                domains = line.split()[1:]
                                dns_info["search_domains"].extend(domains)
            except Exception:
                pass
        
        return dns_info
    
    def _get_network_statistics(self) -> Dict[str, Any]:
        """Get network statistics."""
        try:
            stats = psutil.net_io_counters()
            return {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errin": stats.errin,
                "errout": stats.errout,
                "dropin": stats.dropin,
                "dropout": stats.dropout,
            }
        except Exception:
            return {}
    
    def collect_process_info(self) -> Dict[str, Any]:
        """Collect process information."""
        try:
            processes = []
            max_processes = self.config.max_processes if self.config else 100
            
            for i, proc in enumerate(psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'create_time'])):
                if i >= max_processes:
                    break
                    
                try:
                    process_info = proc.info.copy()
                    if process_info['create_time']:
                        process_info['create_time'] = datetime.fromtimestamp(process_info['create_time']).isoformat()
                    processes.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            # Sort by CPU usage (handle None values)
            processes.sort(key=lambda x: x.get('cpu_percent') or 0, reverse=True)
            
            return {
                "count": len(processes),
                "processes": processes,
                "summary": {
                    "running": len([p for p in processes if p.get('status') == 'running']),
                    "sleeping": len([p for p in processes if p.get('status') == 'sleeping']),
                    "zombie": len([p for p in processes if p.get('status') == 'zombie']),
                },
            }
            
        except Exception as e:
            raise CollectionError(f"Failed to collect process information: {e}")
    
    def collect_security_info(self) -> Dict[str, Any]:
        """Collect security information."""
        return {
            "firewall": self._get_firewall_status(),
            "open_ports": self._get_open_ports(),
            "admin_privileges": self._check_admin_privileges(),
        }
    
    def _get_firewall_status(self) -> Dict[str, Any]:
        """Get firewall status."""
        firewall_info = {"status": "unknown", "details": "Unable to determine"}
        
        try:
            if platform.system() == "Linux":
                # Check ufw
                success, stdout, _ = run_command(["ufw", "status"])
                if success:
                    firewall_info["status"] = "active" if "active" in stdout.lower() else "inactive"
                    firewall_info["details"] = "ufw detected"
                
            elif platform.system() == "Darwin":
                # Check pfctl on macOS
                success, stdout, _ = run_command(["pfctl", "-s", "info"])
                if success:
                    firewall_info["status"] = "active" if "enabled" in stdout.lower() else "inactive"
                    firewall_info["details"] = "pfctl detected"
                    
        except Exception:
            pass
        
        return firewall_info
    
    def _get_open_ports(self) -> List[int]:
        """Get open ports."""
        open_ports = set()
        
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_LISTEN and conn.laddr:
                    open_ports.add(conn.laddr.port)
        except (psutil.AccessDenied, Exception):
            pass
        
        return sorted(list(open_ports))
    
    def _check_admin_privileges(self) -> bool:
        """Check admin privileges."""
        try:
            if platform.system() == "Windows":
                success, _, _ = run_command(["net", "session"])
                return success
            else:
                success, _, _ = run_command(["sudo", "-n", "true"])
                return success
        except Exception:
            pass
        
        return False
    
    def collect_sensor_info(self) -> Dict[str, Any]:
        """Collect sensor information."""
        sensor_info = {
            "temperature": self._get_temperature_sensors(),
            "fans": self._get_fan_sensors(),
            "battery": self._get_battery_info(),
        }
        
        return sensor_info
    
    def _get_temperature_sensors(self) -> Dict[str, Any]:
        """Get temperature sensors."""
        temperatures = {}
        
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                sensors = psutil.sensors_temperatures()
                for name, entries in sensors.items():
                    temp_readings = []
                    for entry in entries:
                        temp_readings.append({
                            "label": entry.label or "N/A",
                            "current": entry.current,
                            "high": entry.high,
                            "critical": entry.critical,
                        })
                    temperatures[name] = temp_readings
        except Exception:
            pass
        
        return temperatures
    
    def _get_fan_sensors(self) -> Dict[str, Any]:
        """Get fan sensors."""
        fans = {}
        
        try:
            if hasattr(psutil, 'sensors_fans'):
                sensors = psutil.sensors_fans()
                for name, entries in sensors.items():
                    fan_readings = []
                    for entry in entries:
                        fan_readings.append({
                            "label": entry.label or "N/A",
                            "current": entry.current,
                        })
                    fans[name] = fan_readings
        except Exception:
            pass
        
        return fans
    
    def collect_python_info(self) -> Dict[str, Any]:
        """Collect Python environment information."""
        try:
            python_info = {
                "version": sys.version,
                "version_info": {
                    "major": sys.version_info.major,
                    "minor": sys.version_info.minor,
                    "micro": sys.version_info.micro,
                    "releaselevel": sys.version_info.releaselevel,
                },
                "executable": sys.executable,
                "prefix": sys.prefix,
                "platform": sys.platform,
                "implementation": {
                    "name": sys.implementation.name,
                    "version": ".".join(map(str, sys.implementation.version[:2])),
                },
                "path_count": len(sys.path),
                "modules_count": len(sys.modules),
                "packages": self._get_installed_packages(),
            }
            
            return python_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect Python information: {e}")
    
    def _get_installed_packages(self) -> List[Dict[str, str]]:
        """Get installed packages."""
        packages = []
        
        # Try using pkg_resources first
        try:
            import pkg_resources
            for dist in pkg_resources.working_set:
                packages.append({
                    "name": dist.project_name,
                    "version": dist.version,
                    "location": dist.location,
                })
        except ImportError:
            # Fallback to pip list
            success, stdout, _ = run_command([sys.executable, "-m", "pip", "list", "--format=json"])
            if success:
                try:
                    packages = json.loads(stdout)
                except json.JSONDecodeError:
                    pass
        
        # Sort by name
        packages.sort(key=lambda x: x.get("name", "").lower())
        
        return packages[:50]  # Limit to 50 packages


# Use the robust collector as the main collector
SystemCollector = RobustSystemCollector
