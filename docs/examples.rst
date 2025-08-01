Examples
========

This page provides practical examples of using Rain CLI in various scenarios.

Basic Usage Examples
--------------------

Simple System Check
~~~~~~~~~~~~~~~~~~~

Get a quick overview of your system:

.. code-block:: bash

   rain

Output example::

   ╭─────────────────────────────────────────────────╮
   │                   RAIN CLI                      │
   │              System Information                 │
   ╰─────────────────────────────────────────────────╯
   
   💻 CPU: Intel(R) Core(TM) i7-9750H @ 2.60GHz
   🔧 Cores: 6 physical, 12 logical
   📊 Usage: 15.2%
   
   🧠 Memory: 8.2 GB / 16.0 GB (48.8% used)
   💾 Swap: 2.1 GB / 4.0 GB (52.5% used)

Real-time Monitoring
~~~~~~~~~~~~~~~~~~~

Monitor your system in real-time:

.. code-block:: bash

   rain --live

This continuously updates the display, useful for:

- Monitoring CPU usage during builds
- Watching memory consumption
- Observing network activity

Machine-Readable Output
~~~~~~~~~~~~~~~~~~~~~~

Get JSON output for scripts:

.. code-block:: bash

   rain --json

.. code-block:: json

   {
     "timestamp": "2024-01-15T14:30:25Z",
     "cpu": {
       "brand": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
       "cores": 6,
       "threads": 12,
       "usage": 15.2,
       "temperature": 45.0
     },
     "memory": {
       "total": "16.0 GB",
       "available": "8.2 GB",
       "used": "7.8 GB",
       "usage": 48.8
     },
     "disks": [
       {
         "device": "/dev/sda1",
         "mountpoint": "/",
         "total": "500.0 GB",
         "free": "125.5 GB",
         "usage": 74.9
       }
     ]
   }

Scripting Examples
------------------

System Health Check Script
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # system_health.sh - Check system health using Rain CLI
   
   JSON_OUTPUT=$(rain --json --quiet)
   
   # Extract values using jq
   CPU_USAGE=$(echo "$JSON_OUTPUT" | jq -r '.cpu.usage')
   MEMORY_USAGE=$(echo "$JSON_OUTPUT" | jq -r '.memory.usage')
   
   echo "System Health Check"
   echo "==================="
   
   # Check CPU usage
   if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
       echo "⚠️  HIGH CPU usage: $CPU_USAGE%"
   else
       echo "✅ CPU usage normal: $CPU_USAGE%"
   fi
   
   # Check memory usage
   if (( $(echo "$MEMORY_USAGE > 90" | bc -l) )); then
       echo "⚠️  HIGH memory usage: $MEMORY_USAGE%"
   else
       echo "✅ Memory usage normal: $MEMORY_USAGE%"
   fi

Disk Space Alert
~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # disk_alert.sh - Alert when disk space is low
   
   rain --json --quiet | jq -r '.disks[] | select(.usage > 85) | 
   "⚠️  Warning: \(.mountpoint) is \(.usage)% full (\(.free) free)"'

Log System Info
~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # log_system.sh - Log system information periodically
   
   LOGFILE="/var/log/system_info.log"
   TIMESTAMP=$(date -Iseconds)
   
   echo "[$TIMESTAMP]" >> "$LOGFILE"
   rain --json --quiet >> "$LOGFILE"
   echo "" >> "$LOGFILE"

Python Integration Examples
---------------------------

System Monitor Dashboard
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import subprocess
   import json
   import time
   from datetime import datetime
   
   def get_system_info():
       """Get system information using Rain CLI"""
       result = subprocess.run(['rain', '--json', '--quiet'], 
                              capture_output=True, text=True)
       return json.loads(result.stdout)
   
   def monitor_system(duration=300, interval=10):
       """Monitor system for specified duration"""
       start_time = time.time()
       
       while time.time() - start_time < duration:
           info = get_system_info()
           timestamp = datetime.now().strftime('%H:%M:%S')
           
           print(f"[{timestamp}] CPU: {info['cpu']['usage']:.1f}% | "
                 f"Memory: {info['memory']['usage']:.1f}% | "
                 f"Temp: {info['cpu'].get('temperature', 'N/A')}°C")
           
           time.sleep(interval)
   
   if __name__ == "__main__":
       monitor_system()

Alert System
~~~~~~~~~~~

.. code-block:: python

   import subprocess
   import json
   import smtplib
   from email.mime.text import MIMEText
   
   def check_system_alerts():
       """Check for system alerts and send email if needed"""
       result = subprocess.run(['rain', '--json', '--quiet'], 
                              capture_output=True, text=True)
       info = json.loads(result.stdout)
       
       alerts = []
       
       # Check CPU usage
       if info['cpu']['usage'] > 80:
           alerts.append(f"High CPU usage: {info['cpu']['usage']:.1f}%")
       
       # Check memory usage
       if info['memory']['usage'] > 90:
           alerts.append(f"High memory usage: {info['memory']['usage']:.1f}%")
       
       # Check disk usage
       for disk in info.get('disks', []):
           if disk['usage'] > 85:
               alerts.append(f"Low disk space on {disk['mountpoint']}: "
                           f"{disk['usage']:.1f}% used")
       
       if alerts:
           send_alert_email(alerts)
   
   def send_alert_email(alerts):
       """Send alert email"""
       # Email configuration would go here
       print("Alerts detected:")
       for alert in alerts:
           print(f"  - {alert}")

PowerShell Examples (Windows)
-----------------------------

System Information Script
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: powershell

   # system_info.ps1 - Get system info using Rain CLI
   
   $json = rain --json --quiet | ConvertFrom-Json
   
   Write-Host "System Information Summary" -ForegroundColor Cyan
   Write-Host "=========================="
   
   Write-Host "CPU: $($json.cpu.brand)" -ForegroundColor Green
   Write-Host "Usage: $($json.cpu.usage)%" -ForegroundColor Yellow
   
   Write-Host "Memory: $($json.memory.used) / $($json.memory.total)" -ForegroundColor Green
   Write-Host "Usage: $($json.memory.usage)%" -ForegroundColor Yellow

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: powershell

   # monitor.ps1 - Monitor system performance
   
   param(
       [int]$Duration = 300,
       [int]$Interval = 5
   )
   
   $startTime = Get-Date
   
   while ((Get-Date) -lt $startTime.AddSeconds($Duration)) {
       $json = rain --json --quiet | ConvertFrom-Json
       $timestamp = Get-Date -Format "HH:mm:ss"
       
       Write-Host "[$timestamp] " -NoNewline
       Write-Host "CPU: $($json.cpu.usage.ToString('F1'))% " -NoNewline -ForegroundColor Green
       Write-Host "Memory: $($json.memory.usage.ToString('F1'))%" -ForegroundColor Yellow
       
       Start-Sleep $Interval
   }

Docker Integration
------------------

Dockerfile with Rain CLI
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

   FROM python:3.9-slim
   
   # Install Rain CLI
   RUN pip install rain-cli
   
   # Add health check using Rain CLI
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD rain --json --quiet > /dev/null || exit 1
   
   # Your application setup here
   COPY . /app
   WORKDIR /app
   
   CMD ["python", "app.py"]

Container Monitoring
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # container_monitor.sh - Monitor containers using Rain CLI
   
   # Run Rain CLI in a container
   docker run --rm -v /proc:/host/proc:ro python:3.9-slim bash -c "
     pip install rain-cli && 
     rain --json --quiet
   "

CI/CD Integration
-----------------

GitHub Actions Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   name: System Information
   on: [push, pull_request]
   
   jobs:
     system-info:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.9'
         
         - name: Install Rain CLI
           run: pip install rain-cli
         
         - name: Collect System Information
           run: |
             echo "## System Information" >> $GITHUB_STEP_SUMMARY
             echo '```json' >> $GITHUB_STEP_SUMMARY
             rain --json --quiet >> $GITHUB_STEP_SUMMARY
             echo '```' >> $GITHUB_STEP_SUMMARY

Jenkins Pipeline
~~~~~~~~~~~~~~~

.. code-block:: groovy

   pipeline {
       agent any
       
       stages {
           stage('System Check') {
               steps {
                   script {
                       sh 'pip install rain-cli'
                       def systemInfo = sh(
                           script: 'rain --json --quiet',
                           returnStdout: true
                       ).trim()
                       
                       echo "System Information: ${systemInfo}"
                   }
               }
           }
       }
   }

Monitoring Integration
---------------------

Prometheus Exporter
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # rain_exporter.py - Prometheus exporter for Rain CLI
   
   import subprocess
   import json
   import time
   from prometheus_client import start_http_server, Gauge
   
   # Define metrics
   cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
   memory_usage = Gauge('system_memory_usage_percent', 'Memory usage percentage')
   disk_usage = Gauge('system_disk_usage_percent', 'Disk usage percentage', ['mountpoint'])
   
   def collect_metrics():
       """Collect metrics using Rain CLI"""
       result = subprocess.run(['rain', '--json', '--quiet'],
                              capture_output=True, text=True)
       data = json.loads(result.stdout)
       
       # Update metrics
       cpu_usage.set(data['cpu']['usage'])
       memory_usage.set(data['memory']['usage'])
       
       for disk in data.get('disks', []):
           disk_usage.labels(mountpoint=disk['mountpoint']).set(disk['usage'])
   
   if __name__ == '__main__':
       # Start HTTP server for Prometheus
       start_http_server(8000)
       
       while True:
           collect_metrics()
           time.sleep(30)

Grafana Dashboard
~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "dashboard": {
       "title": "System Information (Rain CLI)",
       "panels": [
         {
           "title": "CPU Usage",
           "type": "stat",
           "targets": [
             {
               "expr": "system_cpu_usage_percent"
             }
           ]
         },
         {
           "title": "Memory Usage",
           "type": "stat",
           "targets": [
             {
               "expr": "system_memory_usage_percent"
             }
           ]
         }
       ]
     }
   }

These examples demonstrate the versatility of Rain CLI across different platforms and use cases. Whether you're monitoring systems, building dashboards, or integrating into CI/CD pipelines, Rain CLI provides the flexibility and reliability you need.
