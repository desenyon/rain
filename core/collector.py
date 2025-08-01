"""
System information collector for Rain application.
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

try:
    import distro
except ImportError:
    distro = None

try:
    import netifaces
except ImportError:
    netifaces = None

import psutil
import requests

try:
    from uptime import uptime
except ImportError:
    # Fallback uptime calculation
    def uptime():
        return time.time() - psutil.boot_time()

from utils.exceptions import CollectionError
from utils.logger import get_logger

logger = get_logger("collector")


class SystemCollector:
    """Collects comprehensive system information."""
    
    def __init__(self, config=None):
        """Initialize the system collector."""
        self.config = config
        self._cache = {}
        self._cache_timestamps = {}
    
    def collect_all_data(self, sections: List[str]) -> Dict[str, Any]:
        """
        Collect all requested system information.
        
        Args:
            sections: List of sections to collect
            
        Returns:
            Dictionary containing all collected data
        """
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
            system_uptime = timedelta(seconds=uptime())
            
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
                "uptime": str(system_uptime),
                "uptime_seconds": uptime(),
                "current_time": datetime.now().isoformat(),
                "timezone": str(time.tzname),
                "users": [
                    {
                        "name": user.name,
                        "terminal": user.terminal or "N/A",
                        "host": user.host or "local",
                        "started": datetime.fromtimestamp(user.started).isoformat()
                    }
                    for user in psutil.users()
                ],
            }
            
            # Add Linux-specific information
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
            
            # Add environment variables
            system_info["environment"] = dict(sorted(os.environ.items()))
            
            return system_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect system information: {e}")
    
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
        """Get CPU information."""
        try:
            import cpuinfo
            cpu_data = cpuinfo.get_cpu_info()
            
            cpu_info = {
                "brand": cpu_data.get("brand_raw", "Unknown"),
                "model": cpu_data.get("model_name", "Unknown"),
                "architecture": cpu_data.get("arch", "Unknown"),
                "cores": {
                    "physical": psutil.cpu_count(logical=False),
                    "logical": psutil.cpu_count(logical=True),
                },
                "frequency": {
                    "current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                    "min": psutil.cpu_freq().min if psutil.cpu_freq() else None,
                    "max": psutil.cpu_freq().max if psutil.cpu_freq() else None,
                },
                "usage": {
                    "percent": psutil.cpu_percent(interval=1),
                    "per_core": psutil.cpu_percent(interval=1, percpu=True),
                },
                "times": psutil.cpu_times()._asdict(),
                "stats": psutil.cpu_stats()._asdict(),
            }
            
            # Add more CPU details from cpuinfo
            for key in ["vendor_id", "family", "model", "stepping", "flags"]:
                if key in cpu_data:
                    cpu_info[key] = cpu_data[key]
            
            return cpu_info
            
        except ImportError:
            # Fallback without py-cpuinfo
            return {
                "brand": platform.processor(),
                "cores": {
                    "physical": psutil.cpu_count(logical=False),
                    "logical": psutil.cpu_count(logical=True),
                },
                "frequency": {
                    "current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                    "min": psutil.cpu_freq().min if psutil.cpu_freq() else None,
                    "max": psutil.cpu_freq().max if psutil.cpu_freq() else None,
                },
                "usage": {
                    "percent": psutil.cpu_percent(interval=1),
                    "per_core": psutil.cpu_percent(interval=1, percpu=True),
                },
            }
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information."""
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
                "shared": getattr(memory, 'shared', None),
                "slab": getattr(memory, 'slab', None),
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
                "sin": swap.sin,
                "sout": swap.sout,
            }
        }
    
    def _get_disk_info(self) -> List[Dict[str, Any]]:
        """Get disk information."""
        disks = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                disk_info = {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": (usage.used / usage.total) * 100 if usage.total > 0 else 0,
                }
                
                disks.append(disk_info)
                
            except (PermissionError, OSError):
                # Skip inaccessible partitions
                continue
        
        # Add disk I/O statistics
        try:
            disk_io = psutil.disk_io_counters(perdisk=True)
            disk_io_total = psutil.disk_io_counters()
            
            for disk in disks:
                device_name = disk["device"].replace("/dev/", "")
                if device_name in disk_io:
                    io_stats = disk_io[device_name]
                    disk["io"] = {
                        "read_count": io_stats.read_count,
                        "write_count": io_stats.write_count,
                        "read_bytes": io_stats.read_bytes,
                        "write_bytes": io_stats.write_bytes,
                        "read_time": io_stats.read_time,
                        "write_time": io_stats.write_time,
                    }
            
            # Add total disk I/O
            if disk_io_total:
                disks.append({
                    "device": "TOTAL",
                    "io": {
                        "read_count": disk_io_total.read_count,
                        "write_count": disk_io_total.write_count,
                        "read_bytes": disk_io_total.read_bytes,
                        "write_bytes": disk_io_total.write_bytes,
                        "read_time": disk_io_total.read_time,
                        "write_time": disk_io_total.write_time,
                    }
                })
                
        except Exception:
            pass
        
        return disks
    
    def _get_gpu_info(self) -> List[Dict[str, Any]]:
        """Get GPU information."""
        gpus = []
        
        try:
            import GPUtil
            gpu_list = GPUtil.getGPUs()
            
            for gpu in gpu_list:
                gpu_info = {
                    "id": gpu.id,
                    "name": gpu.name,
                    "driver": gpu.driver,
                    "memory": {
                        "total": gpu.memoryTotal,
                        "used": gpu.memoryUsed,
                        "free": gpu.memoryFree,
                        "percent": gpu.memoryUtil * 100,
                    },
                    "temperature": gpu.temperature,
                    "load": gpu.load * 100,
                    "uuid": gpu.uuid,
                }
                gpus.append(gpu_info)
                
        except (ImportError, Exception):
            # Try NVIDIA SMI
            try:
                result = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,temperature.gpu,utilization.gpu", "--format=csv,noheader,nounits"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        parts = line.split(', ')
                        if len(parts) >= 5:
                            gpus.append({
                                "name": parts[0],
                                "memory": {
                                    "total": int(parts[1]),
                                    "used": int(parts[2]),
                                    "percent": (int(parts[2]) / int(parts[1])) * 100,
                                },
                                "temperature": int(parts[3]) if parts[3] != '[Not Supported]' else None,
                                "load": int(parts[4]) if parts[4] != '[Not Supported]' else None,
                            })
                            
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        return gpus
    
    def _get_battery_info(self) -> Optional[Dict[str, Any]]:
        """Get battery information."""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "secsleft": battery.secsleft,
                    "power_plugged": battery.power_plugged,
                    "time_left": str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited",
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
                "routing": self._get_routing_info(),
                "statistics": self._get_network_statistics(),
            }
            
            return network_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect network information: {e}")
    
    def _get_network_interfaces(self) -> List[Dict[str, Any]]:
        """Get network interface information."""
        interfaces = []
        
        if netifaces:
            try:
                for interface_name in netifaces.interfaces():
                    interface_info = {
                        "name": interface_name,
                        "addresses": {},
                        "stats": None,
                    }
                    
                    # Get addresses for each address family
                    addresses = netifaces.ifaddresses(interface_name)
                    for family, addrs in addresses.items():
                        family_name = {
                            netifaces.AF_INET: "ipv4",
                            netifaces.AF_INET6: "ipv6",
                            netifaces.AF_LINK: "mac",
                        }.get(family, f"family_{family}")
                        
                        interface_info["addresses"][family_name] = addrs
                    
                    # Get interface statistics
                    try:
                        stats = psutil.net_io_counters(pernic=True).get(interface_name)
                        if stats:
                            interface_info["stats"] = {
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
                        pass
                    
                    interfaces.append(interface_info)
            except Exception:
                pass
        
        # Fallback: use psutil only
        if not interfaces:
            try:
                stats = psutil.net_io_counters(pernic=True)
                for interface_name, interface_stats in stats.items():
                    interfaces.append({
                        "name": interface_name,
                        "addresses": {},
                        "stats": {
                            "bytes_sent": interface_stats.bytes_sent,
                            "bytes_recv": interface_stats.bytes_recv,
                            "packets_sent": interface_stats.packets_sent,
                            "packets_recv": interface_stats.packets_recv,
                            "errin": interface_stats.errin,
                            "errout": interface_stats.errout,
                            "dropin": interface_stats.dropin,
                            "dropout": interface_stats.dropout,
                        }
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
                    "fd": conn.fd,
                    "family": conn.family.name if hasattr(conn.family, 'name') else str(conn.family),
                    "type": conn.type.name if hasattr(conn.type, 'name') else str(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status,
                    "pid": conn.pid,
                }
                
                # Get process name if available
                if conn.pid:
                    try:
                        process = psutil.Process(conn.pid)
                        connection_info["process_name"] = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        connection_info["process_name"] = None
                
                connections.append(connection_info)
                
        except psutil.AccessDenied:
            logger.warning("Access denied when collecting network connections")
        
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
        dns_info = {
            "servers": [],
            "search_domains": [],
        }
        
        try:
            # Try to read /etc/resolv.conf on Unix systems
            if platform.system() != "Windows":
                resolv_conf = Path("/etc/resolv.conf")
                if resolv_conf.exists():
                    with open(resolv_conf, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("nameserver"):
                                server = line.split()[1]
                                dns_info["servers"].append(server)
                            elif line.startswith("search"):
                                domains = line.split()[1:]
                                dns_info["search_domains"].extend(domains)
            else:
                # Windows DNS resolution
                try:
                    result = subprocess.run(
                        ["nslookup", "localhost"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    # Parse output for DNS servers
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "Server:" in line:
                            server = line.split(':')[1].strip()
                            if server and server != "localhost":
                                dns_info["servers"].append(server)
                except Exception:
                    pass
                    
        except Exception:
            pass
        
        return dns_info
    
    def _get_routing_info(self) -> Dict[str, Any]:
        """Get routing information."""
        routing_info = {
            "default_gateway": None,
            "routes": [],
        }
        
        if netifaces:
            try:
                # Get default gateway
                gateways = netifaces.gateways()
                default_gateway = gateways.get('default')
                if default_gateway and isinstance(default_gateway, dict):
                    ipv4_gateway = default_gateway.get(netifaces.AF_INET)
                    if ipv4_gateway:
                        routing_info["default_gateway"] = {
                            "gateway": ipv4_gateway[0],
                            "interface": ipv4_gateway[1],
                        }
            except Exception:
                pass
        
        return routing_info
    
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
            max_processes = self.config.max_processes if self.config else 1000
            
            for i, proc in enumerate(psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline'])):
                if i >= max_processes:
                    break
                    
                try:
                    process_info = proc.info.copy()
                    process_info['create_time'] = datetime.fromtimestamp(process_info['create_time']).isoformat()
                    process_info['cmdline'] = ' '.join(process_info['cmdline']) if process_info['cmdline'] else ''
                    processes.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            return {
                "count": len(processes),
                "processes": processes[:max_processes],
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
        security_info = {
            "firewall": self._get_firewall_status(),
            "open_ports": self._get_open_ports(),
            "sudo_access": self._check_sudo_access(),
        }
        
        return security_info
    
    def _get_firewall_status(self) -> Dict[str, Any]:
        """Get firewall status."""
        firewall_info = {"status": "unknown", "details": {}}
        
        try:
            if platform.system() == "Linux":
                # Check ufw
                try:
                    result = subprocess.run(
                        ["ufw", "status"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        firewall_info["status"] = "active" if "active" in result.stdout.lower() else "inactive"
                        firewall_info["details"]["ufw"] = result.stdout.strip()
                except FileNotFoundError:
                    pass
                
                # Check iptables
                try:
                    result = subprocess.run(
                        ["iptables", "-L", "-n"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        firewall_info["details"]["iptables"] = "configured"
                except FileNotFoundError:
                    pass
                    
            elif platform.system() == "Darwin":
                # Check pfctl on macOS
                try:
                    result = subprocess.run(
                        ["pfctl", "-s", "info"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        firewall_info["status"] = "active" if "enabled" in result.stdout.lower() else "inactive"
                        firewall_info["details"]["pfctl"] = result.stdout.strip()
                except FileNotFoundError:
                    pass
                    
        except Exception:
            pass
        
        return firewall_info
    
    def _get_open_ports(self) -> List[int]:
        """Get list of open/listening ports."""
        open_ports = set()
        
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_LISTEN and conn.laddr:
                    open_ports.add(conn.laddr.port)
        except psutil.AccessDenied:
            pass
        
        return sorted(list(open_ports))
    
    def _check_sudo_access(self) -> bool:
        """Check if user has sudo access."""
        try:
            if platform.system() != "Windows":
                result = subprocess.run(
                    ["sudo", "-n", "true"],
                    capture_output=True,
                    timeout=2
                )
                return result.returncode == 0
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
        """Get temperature sensor readings."""
        temperatures = {}
        
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                sensors = psutil.sensors_temperatures()
                for name, entries in sensors.items():
                    temp_readings = []
                    for entry in entries:
                        reading = {
                            "label": entry.label or "N/A",
                            "current": entry.current,
                            "high": entry.high,
                            "critical": entry.critical,
                        }
                        temp_readings.append(reading)
                    temperatures[name] = temp_readings
        except Exception:
            pass
        
        return temperatures
    
    def _get_fan_sensors(self) -> Dict[str, Any]:
        """Get fan sensor readings."""
        fans = {}
        
        try:
            if hasattr(psutil, 'sensors_fans'):
                sensors = psutil.sensors_fans()
                for name, entries in sensors.items():
                    fan_readings = []
                    for entry in entries:
                        reading = {
                            "label": entry.label or "N/A",
                            "current": entry.current,
                        }
                        fan_readings.append(reading)
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
                    "serial": sys.version_info.serial,
                },
                "executable": sys.executable,
                "prefix": sys.prefix,
                "base_prefix": getattr(sys, 'base_prefix', sys.prefix),
                "path": sys.path[:10],  # Limit to first 10 entries
                "platform": sys.platform,
                "implementation": {
                    "name": sys.implementation.name,
                    "version": ".".join(map(str, sys.implementation.version[:2])),
                },
                "modules": list(sys.modules.keys())[:50],  # Limit to first 50 modules
                "packages": self._get_installed_packages(),
            }
            
            return python_info
            
        except Exception as e:
            raise CollectionError(f"Failed to collect Python information: {e}")
    
    def _get_installed_packages(self) -> List[Dict[str, str]]:
        """Get list of installed Python packages."""
        packages = []
        
        try:
            import pkg_resources
            
            for dist in pkg_resources.working_set:
                packages.append({
                    "name": dist.project_name,
                    "version": dist.version,
                    "location": dist.location,
                })
                
            # Sort by name
            packages.sort(key=lambda x: x["name"].lower())
            
        except ImportError:
            # Fallback to pip
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "list", "--format=json"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
            except Exception:
                pass
        
        return packages
