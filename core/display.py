"""
Display manager for Rain application using Rich for beautiful terminal output.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from utils.exceptions import DisplayError
from utils.logger import get_logger

logger = get_logger("display")


class DisplayManager:
    """Manages the display of system information using Rich."""
    
    def __init__(self, config=None, console: Optional[Console] = None):
        """Initialize the display manager."""
        self.config = config
        self.console = console or Console()
        
    def display_all(self, data: Dict[str, Any], sections: List[str]) -> None:
        """Display all collected data in a beautiful format."""
        try:
            # Display header
            self._display_header()
            
            # Display each section
            for section in sections:
                if section in data:
                    self._display_section(section, data[section])
                    self.console.print()  # Add spacing between sections
                    
        except Exception as e:
            raise DisplayError(f"Failed to display data: {e}")
    
    def _display_header(self) -> None:
        """Display the application header."""
        from rich.box import DOUBLE_EDGE
        
        # Create beautiful title with colors
        title_text = Text()
        title_text.append("🌧️ ", style="bold bright_blue")
        title_text.append("RAIN", style="bold bright_cyan")
        title_text.append(" SYSTEM REPORT ", style="bold bright_white")
        title_text.append("🌧️", style="bold bright_blue")
        title_text.justify = "center"
        
        subtitle = Text("Comprehensive System Analysis", style="italic bright_white", justify="center")
        timestamp = Text(
            f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            style="dim cyan",
            justify="center"
        )
        
        header_group = Group(
            "",
            title_text,
            subtitle,
            "",
            timestamp,
            ""
        )
        
        header_panel = Panel(
            header_group,
            box=DOUBLE_EDGE,
            border_style="bright_blue",
            padding=(1, 3),
            title="[bold bright_cyan]⚡ SYSTEM INFORMATION ⚡[/bold bright_cyan]",
            title_align="center"
        )
        
        self.console.print(header_panel)
        self.console.print()
    
    def _display_section(self, section_name: str, data: Any) -> None:
        """Display a specific section of data."""
        section_title = section_name.replace("_", " ").title()
        
        if isinstance(data, dict) and "error" in data:
            error_panel = Panel(
                f"[red]Error collecting {section_title}: {data['error']}[/red]",
                title=section_title,
                border_style="red"
            )
            self.console.print(error_panel)
            return
        
        section_methods = {
            "system": self._display_system_info,
            "hardware": self._display_hardware_info,
            "network": self._display_network_info,
            "processes": self._display_process_info,
            "security": self._display_security_info,
            "sensors": self._display_sensor_info,
            "python": self._display_python_info,
        }
        
        display_method = section_methods.get(section_name)
        if display_method:
            display_method(data)
        else:
            # Generic display for unknown sections
            self._display_generic_data(section_title, data)
    
    def _display_system_info(self, data: Dict[str, Any]) -> None:
        """Display system information."""
        from rich.box import ROUNDED
        
        # OS Information Table
        os_table = Table(
            title="🖥️ Operating System",
            show_header=True,
            header_style="bold bright_magenta",
            box=ROUNDED,
            border_style="bright_blue"
        )
        os_table.add_column("Property", style="bright_cyan", width=20)
        os_table.add_column("Value", style="bright_green")
        
        os_info = data.get("os", {})
        os_table.add_row("🏷️ Name", os_info.get("name", "Unknown"))
        os_table.add_row("📦 Release", os_info.get("release", "Unknown"))
        os_table.add_row("🔢 Version", os_info.get("version", "Unknown"))
        os_table.add_row("🏗️ Architecture", " / ".join(os_info.get("architecture", ["Unknown"])))
        os_table.add_row("🌐 Platform", os_info.get("platform", "Unknown"))
        os_table.add_row("⚙️ Processor", os_info.get("processor", "Unknown"))
        
        if "distribution" in os_info:
            dist = os_info["distribution"]
            os_table.add_row("🐧 Distribution", f"{dist.get('name', 'Unknown')} {dist.get('version', '')}")
        
        # System Status Table
        status_table = Table(
            title="📊 System Status",
            show_header=True,
            header_style="bold bright_magenta",
            box=ROUNDED,
            border_style="bright_green"
        )
        status_table.add_column("Property", style="bright_cyan", width=20)
        status_table.add_column("Value", style="bright_yellow")
        
        status_table.add_row("🏠 Hostname", data.get("hostname", "Unknown"))
        status_table.add_row("🌍 FQDN", data.get("fqdn", "Unknown"))
        status_table.add_row("🚀 Boot Time", data.get("boot_time", "Unknown"))
        status_table.add_row("⏱️ Uptime", data.get("uptime", "Unknown"))
        
        # Users Table
        users = data.get("users", [])
        if users:
            users_table = Table(
                title="👥 Current Users",
                show_header=True,
                header_style="bold bright_magenta",
                box=ROUNDED,
                border_style="bright_yellow"
            )
            users_table.add_column("👤 User", style="bright_cyan")
            users_table.add_column("💻 Terminal", style="bright_yellow")
            users_table.add_column("🌐 Host", style="bright_blue")
            users_table.add_column("🕐 Started", style="bright_green")
            
            for user in users:
                users_table.add_row(
                    user.get("name", "Unknown"),
                    user.get("terminal", "N/A"),
                    user.get("host", "local"),
                    user.get("started", "Unknown")
                )
        
        # Display tables in columns
        self.console.print(Columns([os_table, status_table], equal=True, expand=True))
        if users:
            self.console.print(users_table)
    
    def _display_hardware_info(self, data: Dict[str, Any]) -> None:
        """Display hardware information."""
        from rich.box import ROUNDED
        from rich.progress import Progress, BarColumn, TextColumn
        
        # CPU Information
        cpu_data = data.get("cpu", {})
        cpu_table = Table(
            title="🔧 CPU Information",
            show_header=True,
            header_style="bold bright_red",
            box=ROUNDED,
            border_style="bright_red"
        )
        cpu_table.add_column("Property", style="bright_cyan", width=20)
        cpu_table.add_column("Value", style="bright_green")
        
        cpu_table.add_row("🏷️ Brand", cpu_data.get("brand", "Unknown"))
        cpu_table.add_row("🖥️ Model", cpu_data.get("model", "Unknown"))
        cpu_table.add_row("🏗️ Architecture", cpu_data.get("architecture", "Unknown"))
        
        cores = cpu_data.get("cores", {})
        cpu_table.add_row("⚙️ Physical Cores", str(cores.get("physical", "Unknown")))
        cpu_table.add_row("🔄 Logical Cores", str(cores.get("logical", "Unknown")))
        
        usage = cpu_data.get("usage", {})
        cpu_usage = usage.get("percent", 0)
        cpu_table.add_row("📊 CPU Usage", f"[bold bright_{'red' if cpu_usage > 80 else 'yellow' if cpu_usage > 50 else 'green'}]{cpu_usage:.1f}%[/]")
        
        frequency = cpu_data.get("frequency", {})
        if frequency.get("current"):
            cpu_table.add_row("⚡ Current Freq", f"{frequency['current']:.0f} MHz")
        if frequency.get("max"):
            cpu_table.add_row("🚀 Max Freq", f"{frequency['max']:.0f} MHz")
        
        # Memory Information with visual bars
        memory_data = data.get("memory", {})
        memory_table = Table(
            title="💾 Memory Information",
            show_header=True,
            header_style="bold bright_blue",
            box=ROUNDED,
            border_style="bright_blue"
        )
        memory_table.add_column("Type", style="bright_cyan", width=15)
        memory_table.add_column("Total", style="bright_blue", width=12)
        memory_table.add_column("Used", style="bright_red", width=12)
        memory_table.add_column("Free", style="bright_green", width=12)
        memory_table.add_column("Usage", style="bright_yellow", width=20)
        
        virtual = memory_data.get("virtual", {})
        if virtual:
            mem_percent = virtual.get("percent", 0)
            # Create a visual progress bar
            usage_bar = f"{'█' * int(mem_percent/5)}{'░' * (20-int(mem_percent/5))} {mem_percent:.1f}%"
            color = "red" if mem_percent > 80 else "yellow" if mem_percent > 60 else "green"
            
            memory_table.add_row(
                "🗂️ Virtual",
                self._format_bytes(virtual.get("total", 0)),
                self._format_bytes(virtual.get("used", 0)),
                self._format_bytes(virtual.get("free", 0)),
                f"[{color}]{usage_bar}[/{color}]"
            )
        
        swap = memory_data.get("swap", {})
        if swap and swap.get("total", 0) > 0:
            swap_percent = swap.get("percent", 0)
            usage_bar = f"{'█' * int(swap_percent/5)}{'░' * (20-int(swap_percent/5))} {swap_percent:.1f}%"
            color = "red" if swap_percent > 80 else "yellow" if swap_percent > 60 else "green"
            
            memory_table.add_row(
                "🔄 Swap",
                self._format_bytes(swap.get("total", 0)),
                self._format_bytes(swap.get("used", 0)),
                self._format_bytes(swap.get("free", 0)),
                f"[{color}]{usage_bar}[/{color}]"
            )
        
        # Display CPU and Memory side by side
        self.console.print(Columns([cpu_table, memory_table], equal=True, expand=True))
        
        # Disk Information
        disks_data = data.get("disks", [])
        if disks_data:
            disk_table = Table(
                title="💿 Disk Information",
                show_header=True,
                header_style="bold bright_yellow",
                box=ROUNDED,
                border_style="bright_yellow"
            )
            disk_table.add_column("Device", style="bright_cyan", width=20)
            disk_table.add_column("Mount", style="bright_blue", width=15)
            disk_table.add_column("FS", style="bright_yellow", width=8)
            disk_table.add_column("Total", style="bright_green", width=10)
            disk_table.add_column("Used", style="bright_red", width=10)
            disk_table.add_column("Free", style="bright_green", width=10)
            disk_table.add_column("Usage", style="bright_white", width=25)
            
            for disk in disks_data:
                if disk.get("device") != "TOTAL":
                    disk_percent = disk.get("percent", 0)
                    usage_bar = f"{'█' * int(disk_percent/4)}{'░' * (25-int(disk_percent/4))} {disk_percent:.1f}%"
                    color = "red" if disk_percent > 90 else "yellow" if disk_percent > 70 else "green"
                    
                    disk_table.add_row(
                        disk.get("device", "Unknown"),
                        disk.get("mountpoint", "N/A"),
                        disk.get("fstype", "Unknown"),
                        self._format_bytes(disk.get("total", 0)),
                        self._format_bytes(disk.get("used", 0)),
                        self._format_bytes(disk.get("free", 0)),
                        f"[{color}]{usage_bar}[/{color}]"
                    )
            
            self.console.print(disk_table)
        
        # GPU Information
        gpus_data = data.get("gpu", [])
        if gpus_data:
            gpu_table = Table(
                title="🎮 GPU Information",
                show_header=True,
                header_style="bold bright_magenta",
                box=ROUNDED,
                border_style="bright_magenta"
            )
            gpu_table.add_column("Name", style="bright_cyan", width=30)
            gpu_table.add_column("Memory", style="bright_blue", width=15)
            gpu_table.add_column("Usage", style="bright_yellow", width=15)
            gpu_table.add_column("Temperature", style="bright_red", width=12)
            gpu_table.add_column("Load", style="bright_green", width=10)
            
            for gpu in gpus_data:
                memory = gpu.get("memory", {})
                temp_val = gpu.get("temperature")
                load_val = gpu.get("load")
                
                memory_text = "N/A"
                if isinstance(memory.get('total'), (int, float)) and isinstance(memory.get('used'), (int, float)):
                    memory_percent = (memory.get('used', 0) / memory.get('total', 1)) * 100
                    memory_text = f"{memory.get('used', 0)} MB / {memory.get('total', 0)} MB ({memory_percent:.1f}%)"
                
                temp_text = f"🌡️ {temp_val}°C" if temp_val is not None else "N/A"
                load_text = f"⚡ {load_val}%" if load_val is not None else "N/A"
                
                gpu_table.add_row(
                    gpu.get("name", "Unknown"),
                    memory_text,
                    f"{memory_percent:.1f}%" if 'memory_percent' in locals() else "N/A",
                    temp_text,
                    load_text
                )
            
            self.console.print(gpu_table)
        
        # Battery Information
        battery_data = data.get("battery")
        if battery_data:
            battery_table = Table(
                title="🔋 Battery Information",
                show_header=True,
                header_style="bold bright_green",
                box=ROUNDED,
                border_style="bright_green"
            )
            battery_table.add_column("Property", style="bright_cyan", width=20)
            battery_table.add_column("Value", style="bright_green")
            
            battery_percent = battery_data.get("percent", 0)
            charge_bar = f"{'█' * int(battery_percent/5)}{'░' * (20-int(battery_percent/5))} {battery_percent}%"
            charge_color = "red" if battery_percent < 20 else "yellow" if battery_percent < 50 else "green"
            
            battery_table.add_row("🔋 Charge Level", f"[{charge_color}]{charge_bar}[/{charge_color}]")
            battery_table.add_row("🔌 Power Plugged", "✅ Yes" if battery_data.get('power_plugged') else "❌ No")
            battery_table.add_row("⏰ Time Remaining", battery_data.get('time_left', 'Unknown'))
            
            self.console.print(battery_table)
    
    def _display_network_info(self, data: Dict[str, Any]) -> None:
        """Display network information."""
        from rich.box import ROUNDED
        
        # Network Overview with key info
        overview_table = Table(
            title="🌐 Network Overview",
            show_header=True,
            header_style="bold bright_cyan",
            box=ROUNDED,
            border_style="bright_cyan"
        )
        overview_table.add_column("Property", style="bright_cyan", width=20)
        overview_table.add_column("Value", style="bright_green")
        
        overview_table.add_row("🌍 Public IP", data.get("public_ip", "Unknown"))
        
        dns_info = data.get("dns", {})
        dns_servers = ", ".join(dns_info.get("servers", ["Unknown"]))
        overview_table.add_row("🔍 DNS Servers", dns_servers)
        
        routing = data.get("routing", {})
        gateway = routing.get("default_gateway")
        if gateway:
            overview_table.add_row("🚪 Default Gateway", f"{gateway.get('gateway', 'Unknown')} ({gateway.get('interface', 'Unknown')})")
        
        self.console.print(overview_table)
        
        # Network Interfaces
        interfaces = data.get("interfaces", [])
        if interfaces:
            interface_table = Table(
                title="🔌 Network Interfaces",
                show_header=True,
                header_style="bold bright_blue",
                box=ROUNDED,
                border_style="bright_blue"
            )
            interface_table.add_column("Interface", style="bright_cyan", width=15)
            interface_table.add_column("IPv4", style="bright_blue", width=20)
            interface_table.add_column("IPv6", style="bright_magenta", width=25)
            interface_table.add_column("MAC", style="bright_yellow", width=20)
            interface_table.add_column("📤 Sent", style="bright_red", width=12)
            interface_table.add_column("📥 Recv", style="bright_green", width=12)
            
            for interface in interfaces:
                name = interface.get("name", "Unknown")
                addresses = interface.get("addresses", {})
                stats = interface.get("stats", {})
                
                ipv4_addr = "N/A"
                ipv6_addr = "N/A"
                mac_addr = "N/A"
                
                if "ipv4" in addresses and addresses["ipv4"]:
                    ipv4_addr = addresses["ipv4"][0].get("addr", "N/A")
                
                if "ipv6" in addresses and addresses["ipv6"]:
                    ipv6_addr = addresses["ipv6"][0].get("addr", "N/A")
                    if len(ipv6_addr) > 25:
                        ipv6_addr = ipv6_addr[:22] + "..."
                
                if "mac" in addresses and addresses["mac"]:
                    mac_addr = addresses["mac"][0].get("addr", "N/A")
                
                bytes_sent = self._format_bytes(stats.get("bytes_sent", 0)) if stats else "N/A"
                bytes_recv = self._format_bytes(stats.get("bytes_recv", 0)) if stats else "N/A"
                
                # Add emoji based on interface type
                if "wifi" in name.lower() or "wlan" in name.lower():
                    name = f"📶 {name}"
                elif "ethernet" in name.lower() or "eth" in name.lower():
                    name = f"🔗 {name}"
                elif "lo" in name.lower():
                    name = f"🔄 {name}"
                else:
                    name = f"🔌 {name}"
                
                interface_table.add_row(name, ipv4_addr, ipv6_addr, mac_addr, bytes_sent, bytes_recv)
            
            self.console.print(interface_table)
        
        # Network Connections (top 10)
        connections = data.get("connections", [])
        if connections:
            conn_table = Table(
                title="🔗 Active Connections (Top 10)",
                show_header=True,
                header_style="bold bright_yellow",
                box=ROUNDED,
                border_style="bright_yellow"
            )
            conn_table.add_column("Type", style="bright_cyan", width=8)
            conn_table.add_column("Local Address", style="bright_blue", width=22)
            conn_table.add_column("Remote Address", style="bright_red", width=22)
            conn_table.add_column("Status", style="bright_green", width=12)
            conn_table.add_column("Process", style="bright_magenta", width=15)
            
            for conn in connections[:10]:  # Show only top 10
                # Add emoji based on connection type
                conn_type = conn.get("type", "Unknown")
                if conn_type.upper() == "TCP":
                    conn_type = "🌐 TCP"
                elif conn_type.upper() == "UDP":
                    conn_type = "📡 UDP"
                
                # Add status emoji
                status = conn.get("status", "Unknown")
                if status == "ESTABLISHED":
                    status = "🟢 ESTABLISHED"
                elif status == "LISTEN":
                    status = "🔵 LISTEN"
                elif status == "TIME_WAIT":
                    status = "🟡 TIME_WAIT"
                elif status == "CLOSE_WAIT":
                    status = "🟠 CLOSE_WAIT"
                
                conn_table.add_row(
                    conn_type,
                    conn.get("local_address", "N/A"),
                    conn.get("remote_address", "N/A"),
                    status,
                    conn.get("process_name", "Unknown")
                )
            
            self.console.print(conn_table)
    
    def _display_process_info(self, data: Dict[str, Any]) -> None:
        """Display process information."""
        from rich.box import ROUNDED
        
        summary = data.get("summary", {})
        
        # Process Summary with visual elements
        summary_table = Table(
            title="📊 Process Summary",
            show_header=True,
            header_style="bold bright_yellow",
            box=ROUNDED,
            border_style="bright_yellow"
        )
        summary_table.add_column("Status", style="bright_cyan", width=15)
        summary_table.add_column("Count", style="bright_green", width=10)
        summary_table.add_column("Visual", style="bright_white", width=25)
        
        total_count = data.get("count", 0)
        running_count = summary.get("running", 0)
        sleeping_count = summary.get("sleeping", 0)
        zombie_count = summary.get("zombie", 0)
        
        # Create visual bars for process status
        if total_count > 0:
            running_bar = "🟢" * int((running_count / total_count) * 20)
            sleeping_bar = "🔵" * int((sleeping_count / total_count) * 20)
            zombie_bar = "🔴" * int((zombie_count / total_count) * 20) if zombie_count > 0 else ""
        else:
            running_bar = sleeping_bar = zombie_bar = ""
        
        summary_table.add_row("📊 Total", str(total_count), "🔢 All Processes")
        summary_table.add_row("🟢 Running", str(running_count), running_bar or "━")
        summary_table.add_row("💤 Sleeping", str(sleeping_count), sleeping_bar or "━")
        summary_table.add_row("🧟 Zombie", str(zombie_count), zombie_bar or "━")
        
        self.console.print(summary_table)
        
        # Top Processes by CPU with enhanced visuals
        processes = data.get("processes", [])
        if processes:
            proc_table = Table(
                title="🔥 Top Processes by CPU Usage",
                show_header=True,
                header_style="bold bright_red",
                box=ROUNDED,
                border_style="bright_red"
            )
            proc_table.add_column("PID", style="bright_cyan", width=8)
            proc_table.add_column("Name", style="bright_blue", width=20)
            proc_table.add_column("User", style="bright_green", width=15)
            proc_table.add_column("💻 CPU%", style="bright_red", width=12)
            proc_table.add_column("🧠 Memory%", style="bright_yellow", width=15)
            proc_table.add_column("Status", style="bright_magenta", width=12)
            proc_table.add_column("Command", style="bright_white", width=30)
            
            for proc in processes[:20]:  # Show top 20 processes
                cmdline = proc.get("cmdline", "")
                if len(cmdline) > 30:
                    cmdline = cmdline[:27] + "..."
                
                # Add status emoji
                status = proc.get("status", "Unknown")
                if status == "running":
                    status = "🟢 Running"
                elif status == "sleeping":
                    status = "💤 Sleeping"
                elif status == "zombie":
                    status = "🧟 Zombie"
                elif status == "stopped":
                    status = "⏸️ Stopped"
                
                # Create CPU usage visual
                cpu_percent = proc.get('cpu_percent', 0) or 0  # Handle None values
                cpu_visual = f"{'█' * int(cpu_percent/10)}{'░' * (10-int(cpu_percent/10))} {cpu_percent:.1f}%"
                
                # Create memory usage visual
                mem_percent = proc.get('memory_percent', 0) or 0  # Handle None values
                mem_visual = f"{'█' * int(mem_percent/5)}{'░' * (20-int(mem_percent/5))} {mem_percent:.1f}%"
                
                # Color code high usage
                cpu_color = "red" if cpu_percent > 50 else "yellow" if cpu_percent > 20 else "green"
                mem_color = "red" if mem_percent > 50 else "yellow" if mem_percent > 20 else "green"
                
                proc_table.add_row(
                    str(proc.get("pid", 0)),
                    proc.get("name", "Unknown"),
                    proc.get("username", "Unknown"),
                    f"[{cpu_color}]{cpu_visual}[/{cpu_color}]",
                    f"[{mem_color}]{mem_visual}[/{mem_color}]",
                    status,
                    cmdline
                )
            
            self.console.print(proc_table)
    
    def _display_security_info(self, data: Dict[str, Any]) -> None:
        """Display security information."""
        from rich.box import ROUNDED
        
        security_table = Table(
            title="🔒 Security Information",
            show_header=True,
            header_style="bold bright_red",
            box=ROUNDED,
            border_style="bright_red"
        )
        security_table.add_column("Component", style="bright_cyan", width=20)
        security_table.add_column("Status", style="bright_green", width=15)
        security_table.add_column("Details", style="bright_yellow")
        
        # Firewall status with visual indicators
        firewall = data.get("firewall", {})
        firewall_status = firewall.get("status", "unknown")
        if firewall_status == "active":
            status_display = "🟢 Active"
            status_color = "bright_green"
        elif firewall_status == "inactive":
            status_display = "🔴 Inactive"
            status_color = "bright_red" 
        else:
            status_display = "🟡 Unknown"
            status_color = "bright_yellow"
        
        security_table.add_row("🛡️ Firewall", f"[{status_color}]{status_display}[/{status_color}]", "System protection status")
        
        # Open ports with risk assessment
        open_ports = data.get("open_ports", [])
        ports_count = len(open_ports)
        ports_text = ", ".join(map(str, open_ports[:10]))  # Show first 10 ports
        if len(open_ports) > 10:
            ports_text += f" ... (+{len(open_ports) - 10} more)"
        
        # Risk assessment based on number of open ports
        if ports_count == 0:
            port_status = "🟢 None Open"
            port_color = "bright_green"
        elif ports_count <= 5:
            port_status = f"🟡 {ports_count} Open"
            port_color = "bright_yellow"
        else:
            port_status = f"🔴 {ports_count} Open"
            port_color = "bright_red"
        
        security_table.add_row("🚪 Open Ports", f"[{port_color}]{port_status}[/{port_color}]", ports_text or "No open ports detected")
        
        # Sudo access with warning
        sudo_access = data.get("sudo_access", False)
        if sudo_access:
            sudo_display = "🟡 Enabled"
            sudo_color = "bright_yellow"
            sudo_detail = "⚠️ Administrative privileges available"
        else:
            sudo_display = "🟢 Restricted"
            sudo_color = "bright_green"
            sudo_detail = "✅ Standard user permissions"
        
        security_table.add_row("🔑 Sudo Access", f"[{sudo_color}]{sudo_display}[/{sudo_color}]", sudo_detail)
        
        # Additional security checks if available
        if "encryption" in data:
            encryption = data.get("encryption", {})
            if encryption.get("disk_encrypted"):
                security_table.add_row("💾 Disk Encryption", "[bright_green]🟢 Enabled[/bright_green]", "Full disk encryption active")
            else:
                security_table.add_row("💾 Disk Encryption", "[bright_red]🔴 Disabled[/bright_red]", "⚠️ Disk not encrypted")
        
        if "antivirus" in data:
            antivirus = data.get("antivirus", {})
            av_status = antivirus.get("status", "unknown")
            if av_status == "running":
                security_table.add_row("🦠 Antivirus", "[bright_green]🟢 Running[/bright_green]", antivirus.get("name", "Active protection"))
            else:
                security_table.add_row("🦠 Antivirus", "[bright_red]🔴 Not Running[/bright_red]", "⚠️ No active protection detected")
        
        self.console.print(security_table)
    
    def _display_sensor_info(self, data: Dict[str, Any]) -> None:
        """Display sensor information."""
        from rich.box import ROUNDED
        
        # Temperature sensors with visual heat indicators
        temperatures = data.get("temperature", {})
        if temperatures:
            temp_table = Table(
                title="🌡️ Temperature Sensors",
                show_header=True,
                header_style="bold bright_cyan",
                box=ROUNDED,
                border_style="bright_cyan"
            )
            temp_table.add_column("Sensor", style="bright_cyan", width=20)
            temp_table.add_column("Label", style="bright_blue", width=15)
            temp_table.add_column("Current", style="bright_red", width=15)
            temp_table.add_column("Status", style="bright_yellow", width=15)
            temp_table.add_column("Limits", style="bright_white", width=20)
            
            for sensor_name, readings in temperatures.items():
                for reading in readings:
                    current_temp = reading.get('current', 0)
                    high_temp = reading.get('high')
                    critical_temp = reading.get('critical')
                    
                    # Temperature status with emojis
                    if critical_temp and current_temp >= critical_temp:
                        temp_status = "🔥 Critical"
                        temp_color = "bright_red"
                    elif high_temp and current_temp >= high_temp:
                        temp_status = "🟡 High"
                        temp_color = "bright_yellow"
                    elif current_temp >= 70:
                        temp_status = "🟠 Warm"
                        temp_color = "yellow"
                    else:
                        temp_status = "🟢 Normal"
                        temp_color = "bright_green"
                    
                    # Create temperature bar
                    temp_bar = "🔥" * int(current_temp/20) if current_temp > 0 else "❄️"
                    
                    limits_text = f"H:{high_temp}°C" if high_temp else "N/A"
                    if critical_temp:
                        limits_text += f" C:{critical_temp}°C"
                    
                    temp_table.add_row(
                        sensor_name,
                        reading.get("label", "N/A"),
                        f"[{temp_color}]{current_temp:.1f}°C {temp_bar}[/{temp_color}]",
                        f"[{temp_color}]{temp_status}[/{temp_color}]",
                        limits_text
                    )
            
            self.console.print(temp_table)
        
        # Fan sensors with RPM visualization
        fans = data.get("fans", {})
        if fans:
            fan_table = Table(
                title="🌀 Fan Sensors",
                show_header=True,
                header_style="bold bright_blue",
                box=ROUNDED,
                border_style="bright_blue"
            )
            fan_table.add_column("Sensor", style="bright_cyan", width=20)
            fan_table.add_column("Label", style="bright_blue", width=15)
            fan_table.add_column("Speed", style="bright_green", width=20)
            fan_table.add_column("Status", style="bright_yellow", width=15)
            
            for sensor_name, readings in fans.items():
                for reading in readings:
                    rpm = reading.get('current', 0)
                    
                    # Fan speed visualization
                    if rpm > 3000:
                        speed_status = "🌪️ High Speed"
                        speed_color = "bright_red"
                        speed_icon = "🔴🔴🔴"
                    elif rpm > 1500:
                        speed_status = "💨 Medium Speed"
                        speed_color = "bright_yellow"
                        speed_icon = "🟡🟡"
                    elif rpm > 500:
                        speed_status = "🌬️ Low Speed"
                        speed_color = "bright_green"
                        speed_icon = "🟢"
                    else:
                        speed_status = "⭕ Idle/Off"
                        speed_color = "bright_white"
                        speed_icon = "⚪"
                    
                    fan_table.add_row(
                        sensor_name,
                        reading.get("label", "N/A"),
                        f"[{speed_color}]{rpm:.0f} RPM {speed_icon}[/{speed_color}]",
                        f"[{speed_color}]{speed_status}[/{speed_color}]"
                    )
            
            self.console.print(fan_table)
        
        # Power/Battery sensors if available
        power = data.get("power", {})
        if power:
            power_table = Table(
                title="⚡ Power Sensors",
                show_header=True,
                header_style="bold bright_yellow",
                box=ROUNDED,
                border_style="bright_yellow"
            )
            power_table.add_column("Sensor", style="bright_cyan", width=20)
            power_table.add_column("Type", style="bright_blue", width=15)
            power_table.add_column("Value", style="bright_green", width=20)
            power_table.add_column("Status", style="bright_yellow", width=15)
            
            for sensor_name, readings in power.items():
                if isinstance(readings, list):
                    for reading in readings:
                        power_value = reading.get('current', 0)
                        power_unit = reading.get('unit', 'W')
                        
                        # Power consumption status
                        if power_unit == 'W' and power_value > 100:
                            power_status = "🔴 High Power"
                            power_color = "bright_red"
                        elif power_unit == 'W' and power_value > 50:
                            power_status = "🟡 Medium Power"
                            power_color = "bright_yellow"
                        else:
                            power_status = "🟢 Normal"
                            power_color = "bright_green"
                        
                        power_table.add_row(
                            sensor_name,
                            reading.get("type", "Power"),
                            f"[{power_color}]{power_value:.2f} {power_unit}[/{power_color}]",
                            f"[{power_color}]{power_status}[/{power_color}]"
                        )
            
            self.console.print(power_table)
    
    def _display_python_info(self, data: Dict[str, Any]) -> None:
        """Display Python environment information."""
        from rich.box import ROUNDED
        
        # Python Version and Environment
        python_table = Table(
            title="🐍 Python Environment",
            show_header=True,
            header_style="bold bright_green",
            box=ROUNDED,
            border_style="bright_green"
        )
        python_table.add_column("Property", style="bright_cyan", width=20)
        python_table.add_column("Value", style="bright_green")
        
        # Extract version number and add emoji
        version_full = data.get("version", "Unknown")
        version_short = version_full.split()[0] if version_full != "Unknown" else "Unknown"
        python_table.add_row("🏷️ Version", version_short)
        
        executable = data.get("executable", "Unknown")
        # Truncate long paths
        if len(executable) > 50:
            executable = "..." + executable[-47:]
        python_table.add_row("📂 Executable", executable)
        
        python_table.add_row("🖥️ Platform", data.get("platform", "Unknown"))
        
        implementation = data.get("implementation", {})
        impl_name = implementation.get('name', 'Unknown')
        impl_version = implementation.get('version', '')
        python_table.add_row("⚙️ Implementation", f"{impl_name} {impl_version}")
        
        prefix = data.get("prefix", "Unknown")
        if len(prefix) > 50:
            prefix = "..." + prefix[-47:]
        python_table.add_row("📁 Prefix", prefix)
        
        # Virtual environment detection
        if "venv" in executable.lower() or "virtualenv" in executable.lower():
            python_table.add_row("🌐 Environment", "[bright_blue]📦 Virtual Environment[/bright_blue]")
        elif "conda" in executable.lower():
            python_table.add_row("🌐 Environment", "[bright_yellow]🅰️ Conda Environment[/bright_yellow]")
        else:
            python_table.add_row("🌐 Environment", "[bright_white]🖥️ System Python[/bright_white]")
        
        self.console.print(python_table)
        
        # Installed Packages with enhanced display
        packages = data.get("packages", [])
        if packages:
            pkg_table = Table(
                title=f"📦 Installed Packages (Top 20 of {len(packages)})",
                show_header=True,
                header_style="bold bright_blue",
                box=ROUNDED,
                border_style="bright_blue"
            )
            pkg_table.add_column("Package", style="bright_cyan", width=25)
            pkg_table.add_column("Version", style="bright_blue", width=15)
            pkg_table.add_column("Type", style="bright_yellow", width=12)
            pkg_table.add_column("Location", style="bright_white")
            
            for package in packages[:20]:
                pkg_name = package.get("name", "Unknown")
                pkg_version = package.get("version", "Unknown")
                location = package.get("location", "Unknown")
                
                # Determine package type and add emoji
                if any(keyword in pkg_name.lower() for keyword in ['django', 'flask', 'fastapi']):
                    pkg_type = "🌐 Web"
                elif any(keyword in pkg_name.lower() for keyword in ['numpy', 'pandas', 'matplotlib', 'scipy']):
                    pkg_type = "📊 Data"
                elif any(keyword in pkg_name.lower() for keyword in ['pytest', 'unittest', 'mock']):
                    pkg_type = "🧪 Test"
                elif any(keyword in pkg_name.lower() for keyword in ['requests', 'urllib', 'http']):
                    pkg_type = "🌍 HTTP"
                elif any(keyword in pkg_name.lower() for keyword in ['pip', 'setuptools', 'wheel']):
                    pkg_type = "⚙️ Tool"
                else:
                    pkg_type = "📦 Lib"
                
                # Truncate long locations
                if len(location) > 35:
                    location = "..." + location[-32:]
                
                # Add popular package emojis
                if pkg_name.lower() in ['numpy', 'pandas', 'matplotlib']:
                    pkg_name = f"⭐ {pkg_name}"
                elif pkg_name.lower() in ['django', 'flask', 'fastapi']:
                    pkg_name = f"🚀 {pkg_name}"
                elif pkg_name.lower() in ['requests', 'urllib3']:
                    pkg_name = f"🔗 {pkg_name}"
                
                pkg_table.add_row(pkg_name, pkg_version, pkg_type, location)
            
            self.console.print(pkg_table)
            
            # Package statistics
            if len(packages) > 20:
                stats_table = Table(
                    title="📈 Package Statistics",
                    show_header=True,
                    header_style="bold bright_magenta",
                    box=ROUNDED,
                    border_style="bright_magenta"
                )
                stats_table.add_column("Metric", style="bright_cyan", width=20)
                stats_table.add_column("Count", style="bright_green", width=10)
                stats_table.add_column("Percentage", style="bright_yellow", width=15)
                
                total_packages = len(packages)
                
                # Count package types
                web_packages = sum(1 for pkg in packages if any(keyword in pkg.get("name", "").lower() 
                                  for keyword in ['django', 'flask', 'fastapi', 'web']))
                data_packages = sum(1 for pkg in packages if any(keyword in pkg.get("name", "").lower() 
                                   for keyword in ['numpy', 'pandas', 'matplotlib', 'scipy', 'data']))
                test_packages = sum(1 for pkg in packages if any(keyword in pkg.get("name", "").lower() 
                                   for keyword in ['pytest', 'test', 'mock', 'unittest']))
                
                stats_table.add_row("📊 Total Packages", str(total_packages), "100%")
                if web_packages > 0:
                    stats_table.add_row("🌐 Web Packages", str(web_packages), f"{(web_packages/total_packages)*100:.1f}%")
                if data_packages > 0:
                    stats_table.add_row("📈 Data Packages", str(data_packages), f"{(data_packages/total_packages)*100:.1f}%")
                if test_packages > 0:
                    stats_table.add_row("🧪 Test Packages", str(test_packages), f"{(test_packages/total_packages)*100:.1f}%")
                
                self.console.print(stats_table)
                
                pkg_table.add_row(
                    package.get("name", "Unknown"),
                    package.get("version", "Unknown"),
                    location
                )
            
            if len(packages) > 20:
                pkg_table.add_row("...", f"(+{len(packages) - 20} more packages)", "")
            
            self.console.print(pkg_table)
    
    def _display_generic_data(self, title: str, data: Any) -> None:
        """Display generic data in a tree format."""
        panel = Panel(self._create_tree_from_data(data), title=title, border_style="blue")
        self.console.print(panel)
    
    def _create_tree_from_data(self, data: Any, parent_tree: Optional[Tree] = None) -> Tree:
        """Create a tree representation of data."""
        if parent_tree is None:
            tree = Tree("Data")
        else:
            tree = parent_tree
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    branch = tree.add(f"[cyan]{key}[/cyan]")
                    self._create_tree_from_data(value, branch)
                else:
                    tree.add(f"[cyan]{key}[/cyan]: [green]{value}[/green]")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    branch = tree.add(f"[yellow]Item {i}[/yellow]")
                    self._create_tree_from_data(item, branch)
                else:
                    tree.add(f"[yellow]Item {i}[/yellow]: [green]{item}[/green]")
        else:
            tree.add(f"[green]{data}[/green]")
        
        return tree
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format."""
        value = float(bytes_value)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024.0:
                return f"{value:.1f} {unit}"
            value /= 1024.0
        return f"{value:.1f} PB"
    
    def _format_percentage(self, value: float) -> str:
        """Format percentage value."""
        return f"{value:.1f}%"
    
    def run_live_monitor(self, collector, sections: List[str]) -> None:
        """Run live monitoring mode."""
        try:
            with Live(self._create_live_layout(), refresh_per_second=0.5, screen=True) as live:
                while True:
                    try:
                        data = collector.collect_all_data(sections)
                        layout = self._create_live_layout_with_data(data, sections)
                        live.update(layout)
                        time.sleep(self.config.live_update_interval if self.config else 2.0)
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        logger.error(f"Error in live monitoring: {e}")
                        time.sleep(1.0)
                        
        except Exception as e:
            raise DisplayError(f"Failed to run live monitor: {e}")
    
    def _create_live_layout(self) -> Layout:
        """Create the live monitoring layout."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(Panel("Rain 🌧️ - Live Monitoring", style="bold blue"))
        layout["footer"].update(Panel("Press Ctrl+C to exit", style="dim"))
        
        return layout
    
    def _create_live_layout_with_data(self, data: Dict[str, Any], sections: List[str]) -> Layout:
        """Create live layout with actual data."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        # Header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_text = f"Rain 🌧️ - Live Monitoring | {timestamp}"
        layout["header"].update(Panel(header_text, style="bold blue"))
        
        # Main content
        if len(sections) == 1:
            # Single section view
            section_data = data.get(sections[0], {})
            content = self._create_live_section_content(sections[0], section_data)
            layout["main"].update(content)
        else:
            # Multi-section view
            layout["main"].split_row(
                *[Layout(name=f"section_{i}") for i in range(min(len(sections), 3))]
            )
            
            for i, section in enumerate(sections[:3]):  # Show max 3 sections side by side
                section_data = data.get(section, {})
                content = self._create_live_section_content(section, section_data)
                layout[f"section_{i}"].update(content)
        
        # Footer
        layout["footer"].update(Panel("Press Ctrl+C to exit | Live updates every 2 seconds", style="dim"))
        
        return layout
    
    def _create_live_section_content(self, section_name: str, data: Any) -> Panel:
        """Create content for a live monitoring section."""
        if section_name == "hardware":
            return self._create_live_hardware_panel(data)
        elif section_name == "network":
            return self._create_live_network_panel(data)
        elif section_name == "processes":
            return self._create_live_processes_panel(data)
        else:
            # Generic content
            content = self._create_tree_from_data(data)
            return Panel(content, title=section_name.title(), border_style="blue")
    
    def _create_live_hardware_panel(self, data: Dict[str, Any]) -> Panel:
        """Create live hardware monitoring panel."""
        content_parts = []
        
        # CPU usage
        cpu = data.get("cpu", {})
        cpu_usage = cpu.get("usage", {}).get("percent", 0)
        content_parts.append(f"[bold red]CPU:[/bold red] {cpu_usage:.1f}%")
        
        # Memory usage
        memory = data.get("memory", {})
        virtual = memory.get("virtual", {})
        memory_percent = virtual.get("percent", 0)
        memory_used = self._format_bytes(virtual.get("used", 0))
        memory_total = self._format_bytes(virtual.get("total", 0))
        content_parts.append(f"[bold blue]Memory:[/bold blue] {memory_percent:.1f}% ({memory_used}/{memory_total})")
        
        # Temperature (if available)
        temperatures = data.get("temperature", {})
        if temperatures:
            for sensor_name, readings in temperatures.items():
                if readings:
                    temp = readings[0].get("current", 0)
                    content_parts.append(f"[bold yellow]Temp ({sensor_name}):[/bold yellow] {temp:.1f}°C")
                    break  # Show only first temperature sensor
        
        content = "\n".join(content_parts)
        return Panel(content, title="Hardware Monitor", border_style="red")
    
    def _create_live_network_panel(self, data: Dict[str, Any]) -> Panel:
        """Create live network monitoring panel."""
        content_parts = []
        
        # Public IP
        public_ip = data.get("public_ip", "Unknown")
        content_parts.append(f"[bold blue]Public IP:[/bold blue] {public_ip}")
        
        # Active connections count
        connections = data.get("connections", [])
        content_parts.append(f"[bold green]Active Connections:[/bold green] {len(connections)}")
        
        # Network statistics
        stats = data.get("statistics", {})
        if stats:
            bytes_sent = self._format_bytes(stats.get("bytes_sent", 0))
            bytes_recv = self._format_bytes(stats.get("bytes_recv", 0))
            content_parts.append(f"[bold yellow]Sent:[/bold yellow] {bytes_sent}")
            content_parts.append(f"[bold cyan]Received:[/bold cyan] {bytes_recv}")
        
        content = "\n".join(content_parts)
        return Panel(content, title="Network Monitor", border_style="blue")
    
    def _create_live_processes_panel(self, data: Dict[str, Any]) -> Panel:
        """Create live processes monitoring panel."""
        content_parts = []
        
        # Process count
        total_processes = data.get("count", 0)
        content_parts.append(f"[bold green]Total Processes:[/bold green] {total_processes}")
        
        # Top processes
        processes = data.get("processes", [])
        content_parts.append("[bold yellow]Top CPU Users:[/bold yellow]")
        
        for proc in processes[:5]:  # Show top 5
            name = proc.get("name", "Unknown")
            cpu_percent = proc.get("cpu_percent", 0)
            content_parts.append(f"  {name}: {cpu_percent:.1f}%")
        
        content = "\n".join(content_parts)
        return Panel(content, title="Process Monitor", border_style="yellow")
    
    def output_json(self, data: Dict[str, Any]) -> None:
        """Output data in JSON format."""
        try:
            json_output = json.dumps(data, indent=2, default=str)
            # Use plain print to avoid Rich formatting/coloring
            print(json_output)
        except Exception as e:
            raise DisplayError(f"Failed to output JSON: {e}")
    
    def save_to_file(self, data: Dict[str, Any], file_path: str, sections: List[str]) -> None:
        """Save data to a file."""
        try:
            output_path = Path(file_path)
            
            if output_path.suffix.lower() == '.json':
                # Save as JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
            else:
                # Save as formatted text
                # Temporarily capture console output
                from io import StringIO
                from contextlib import redirect_stdout
                
                string_buffer = StringIO()
                temp_console = Console(file=string_buffer, width=120)
                temp_display = DisplayManager(self.config, temp_console)
                
                temp_display._display_header()
                for section in sections:
                    if section in data:
                        temp_display._display_section(section, data[section])
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(string_buffer.getvalue())
            
            self.console.print(f"[green]Data saved to {output_path}[/green]")
            
        except Exception as e:
            raise DisplayError(f"Failed to save data to file: {e}")
