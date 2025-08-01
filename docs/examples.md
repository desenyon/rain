# Examples

This page provides practical examples of using Rain CLI in various scenarios.

## Basic Examples

### Simple System Check

```bash
# Quick system overview
rain -s system

# Check hardware specs
rain -s hardware

# View running processes
rain -s processes
```

### Generating Reports

```bash
# Full system report
rain --save full-report.txt

# JSON report for automation
rain --json --save system-data.json

# Specific sections report
rain -s system -s hardware -s security --save audit-report.txt
```

## Monitoring Examples

### Real-time System Monitoring

```bash
# Live monitoring all sections
rain --live

# Monitor specific components
rain --live -s hardware -s processes

# Clean live monitoring (no banner)
rain --live --no-banner -s hardware
```

### Automated Monitoring Script

```bash
#!/bin/bash
# daily-check.sh - Daily system health check

DATE=$(date +%Y%m%d)
REPORT_DIR="/var/log/rain-reports"
mkdir -p "$REPORT_DIR"

# Generate daily report
rain --json -s all > "$REPORT_DIR/system-report-$DATE.json"

# Check for high CPU usage
CPU_USAGE=$(rain --json -s hardware --no-banner | jq '.hardware.cpu.usage.percent')
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "ALERT: High CPU usage detected: $CPU_USAGE%" | mail -s "CPU Alert" admin@example.com
fi

# Check available disk space
rain -s hardware --no-banner | grep -i "disk" > "$REPORT_DIR/disk-status-$DATE.txt"
```

## Development Examples

### Python Environment Check

```bash
# Check Python environment
rain -s python

# Detailed Python info with packages
rain -s python --save python-env.txt

# JSON output for analysis
rain -s python --json | jq '.python.packages | length'
```

### Development Monitoring

```bash
# Monitor during development
rain --live -s hardware -s processes | grep python

# Check system impact of your application
rain -s processes --no-banner | grep myapp
```

## Security Examples

### Security Audit

```bash
# Basic security check
rain -s security

# Comprehensive security audit
rain -s security -s network -s processes --save security-audit.txt

# Check open ports and connections
rain -s network --no-banner | grep -E "(connections|ports)"
```

### Network Analysis

```bash
# Network interface status
rain -s network

# Public IP and connectivity
rain -s network --json | jq '.network.public_ip'

# Network statistics
rain -s network --save network-stats.txt
```

## System Administration Examples

### Server Health Check

```bash
#!/bin/bash
# server-health.sh - Comprehensive server health check

echo "=== Server Health Check ===" > health-report.txt
echo "Date: $(date)" >> health-report.txt
echo "" >> health-report.txt

# System information
echo "=== System Information ===" >> health-report.txt
rain -s system --no-banner >> health-report.txt
echo "" >> health-report.txt

# Hardware status
echo "=== Hardware Status ===" >> health-report.txt
rain -s hardware --no-banner >> health-report.txt
echo "" >> health-report.txt

# Top processes
echo "=== Top Processes ===" >> health-report.txt
rain -s processes --no-banner | head -20 >> health-report.txt
echo "" >> health-report.txt

# Security status
echo "=== Security Status ===" >> health-report.txt
rain -s security --no-banner >> health-report.txt

echo "Health check completed. Report saved to health-report.txt"
```

### Performance Monitoring

```bash
# Monitor performance over time
while true; do
    echo "$(date): $(rain --json -s hardware --no-banner | jq -r '.hardware.cpu.usage.percent')%" >> cpu-usage.log
    sleep 60
done

# Memory usage tracking
rain --live -s hardware | grep -i memory | tee memory-usage.log
```

## Integration Examples

### Monitoring Integration

```python
#!/usr/bin/env python3
# monitoring-integration.py
import json
import subprocess
import requests
import time

def get_system_metrics():
    """Get system metrics using Rain CLI"""
    result = subprocess.run(
        ['rain', '--json', '-s', 'hardware', '--no-banner'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def send_to_monitoring_system(metrics):
    """Send metrics to monitoring system"""
    payload = {
        'timestamp': time.time(),
        'cpu_usage': metrics['hardware']['cpu']['usage']['percent'],
        'memory_usage': metrics['hardware']['memory']['virtual']['percent'],
        'host': metrics['hardware'].get('hostname', 'unknown')
    }
    
    # Send to monitoring endpoint
    response = requests.post(
        'https://monitoring.example.com/api/metrics',
        json=payload
    )
    return response.status_code == 200

def main():
    while True:
        try:
            metrics = get_system_metrics()
            if send_to_monitoring_system(metrics):
                print("Metrics sent successfully")
            else:
                print("Failed to send metrics")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(300)  # Every 5 minutes

if __name__ == "__main__":
    main()
```

### Alerting System

```python
#!/usr/bin/env python3
# alerting-system.py
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

class SystemAlerting:
    def __init__(self, smtp_server, smtp_port, username, password, recipients):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipients = recipients
    
    def get_system_data(self):
        """Get system data using Rain CLI"""
        result = subprocess.run(
            ['rain', '--json', '-s', 'all', '--no-banner'],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    
    def check_alerts(self, data):
        """Check for alert conditions"""
        alerts = []
        
        # CPU usage alert
        cpu_usage = data['hardware']['cpu']['usage']['percent']
        if cpu_usage > 80:
            alerts.append(f"High CPU usage: {cpu_usage:.1f}%")
        
        # Memory usage alert
        memory_usage = data['hardware']['memory']['virtual']['percent']
        if memory_usage > 85:
            alerts.append(f"High memory usage: {memory_usage:.1f}%")
        
        # Disk usage alert
        for disk in data['hardware']['disks']:
            if disk.get('usage', {}).get('percent', 0) > 90:
                alerts.append(f"High disk usage on {disk['mountpoint']}: {disk['usage']['percent']:.1f}%")
        
        return alerts
    
    def send_alert(self, alerts):
        """Send alert email"""
        if not alerts:
            return
        
        subject = f"System Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = "System alerts detected:\n\n" + "\n".join(f"• {alert}" for alert in alerts)
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = ', '.join(self.recipients)
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
    
    def run(self):
        """Run the alerting system"""
        try:
            data = self.get_system_data()
            alerts = self.check_alerts(data)
            self.send_alert(alerts)
            
            if alerts:
                print(f"Sent {len(alerts)} alerts")
            else:
                print("No alerts")
                
        except Exception as e:
            print(f"Error: {e}")

# Usage
if __name__ == "__main__":
    alerting = SystemAlerting(
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        username="your-email@gmail.com",
        password="your-app-password",
        recipients=["admin@example.com"]
    )
    alerting.run()
```

### Log Analysis

```bash
#!/bin/bash
# log-analysis.sh - Analyze system logs with Rain CLI context

# Get current system state
rain --json -s all --no-banner > current-state.json

# Extract key metrics
CPU=$(jq -r '.hardware.cpu.usage.percent' current-state.json)
MEMORY=$(jq -r '.hardware.memory.virtual.percent' current-state.json)
UPTIME=$(jq -r '.system.uptime' current-state.json)

# Log to syslog with context
logger "RAIN_METRICS: CPU=${CPU}% Memory=${MEMORY}% Uptime=${UPTIME}"

# Analyze recent logs with system context
echo "System Metrics at $(date):" > analysis.log
echo "CPU Usage: ${CPU}%" >> analysis.log
echo "Memory Usage: ${MEMORY}%" >> analysis.log
echo "System Uptime: ${UPTIME}" >> analysis.log
echo "" >> analysis.log
echo "Recent System Logs:" >> analysis.log
journalctl --since "1 hour ago" --no-pager >> analysis.log
```

## Automation Examples

### Cron Job Setup

```bash
# Add to crontab (crontab -e)

# Daily system report at 6 AM
0 6 * * * /usr/local/bin/rain --json -s all --no-banner > /var/log/daily-system-$(date +\%Y\%m\%d).json

# Hourly resource monitoring
0 * * * * /usr/local/bin/rain --json -s hardware --no-banner | jq '.hardware.cpu.usage.percent' >> /var/log/cpu-usage.log

# Weekly comprehensive report
0 0 * * 0 /usr/local/bin/rain -s all --save /var/log/weekly-report-$(date +\%Y\%m\%d).txt
```

### Systemd Service

```ini
# /etc/systemd/system/rain-monitoring.service
[Unit]
Description=Rain System Monitoring
After=network.target

[Service]
Type=simple
User=monitoring
ExecStart=/usr/local/bin/python3 /opt/monitoring/rain-monitor.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

```python
# /opt/monitoring/rain-monitor.py
import time
import json
import subprocess
from pathlib import Path

def main():
    log_dir = Path("/var/log/rain-monitoring")
    log_dir.mkdir(exist_ok=True)
    
    while True:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Collect system data
        result = subprocess.run(
            ['rain', '--json', '-s', 'hardware', '-s', 'processes', '--no-banner'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            log_file = log_dir / f"system_data_{timestamp}.json"
            
            with open(log_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"System data logged to {log_file}")
        else:
            print(f"Error collecting data: {result.stderr}")
        
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()
```

These examples demonstrate the versatility and power of Rain CLI for various system administration, monitoring, and automation tasks.
