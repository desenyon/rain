User Guide
==========

Rain CLI is a beautiful command-line tool that displays comprehensive system information. This guide will help you get the most out of its features.

Quick Start
-----------

The simplest way to use Rain CLI is to run it without any arguments:

.. code-block:: bash

   rain

This will display a beautiful, color-coded overview of your system including:

- CPU information
- Memory usage
- Disk usage
- Network interfaces
- Operating system details
- Hardware specifications

Display Options
---------------

Rain CLI offers several display modes to suit different use cases:

Live Mode
~~~~~~~~~

Watch your system information update in real-time:

.. code-block:: bash

   rain --live

This mode continuously refreshes the display, perfect for monitoring system performance.

JSON Output
~~~~~~~~~~~

Get machine-readable output for scripts and automation:

.. code-block:: bash

   rain --json

Example output:

.. code-block:: json

   {
     "cpu": {
       "brand": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
       "cores": 6,
       "threads": 12,
       "usage": 15.2
     },
     "memory": {
       "total": "16.0 GB",
       "available": "8.2 GB",
       "usage": 48.8
     }
   }

Quiet Mode
~~~~~~~~~~

Suppress the banner and extra formatting:

.. code-block:: bash

   rain --quiet

This is useful when you want just the information without decorative elements.

Understanding the Output
------------------------

System Overview
~~~~~~~~~~~~~~~

The default output is organized into several sections:

**CPU Information**
   - Processor brand and model
   - Number of cores and threads
   - Current usage percentage
   - Temperature (if available)

**Memory Information**
   - Total RAM
   - Available memory
   - Usage percentage
   - Swap usage (if configured)

**Disk Information**
   - Available drives/partitions
   - Total capacity
   - Free space
   - Usage percentage

**Network Information**
   - Active network interfaces
   - IP addresses
   - Network statistics (if available)

**System Information**
   - Operating system
   - Kernel version
   - Uptime
   - Boot time

Color Coding
~~~~~~~~~~~~

Rain CLI uses colors to help you quickly identify different types of information:

- **Green**: Normal/healthy values
- **Yellow**: Warning levels (moderate usage)
- **Red**: Critical levels (high usage)
- **Blue**: Informational text
- **Cyan**: Headers and labels

Advanced Usage
--------------

Integration with Scripts
~~~~~~~~~~~~~~~~~~~~~~~~

Rain CLI works well in automation scripts. Here's a bash example:

.. code-block:: bash

   #!/bin/bash
   
   # Get CPU usage as JSON
   CPU_USAGE=$(rain --json --quiet | jq '.cpu.usage')
   
   if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
       echo "High CPU usage detected: $CPU_USAGE%"
       # Send alert
   fi

Monitoring with Watch
~~~~~~~~~~~~~~~~~~~~~

Combine with the ``watch`` command for periodic updates:

.. code-block:: bash

   watch -n 5 'rain --quiet'

This runs Rain CLI every 5 seconds.

Custom Refresh Rate in Live Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The live mode updates every 2 seconds by default. This can be adjusted in future versions.

Troubleshooting
---------------

Permission Issues
~~~~~~~~~~~~~~~~~

Some system information requires elevated privileges:

.. code-block:: bash

   sudo rain

Missing Information
~~~~~~~~~~~~~~~~~~~

If certain information is missing:

1. Install optional dependencies (see Installation guide)
2. Check if your system supports the feature
3. Run with elevated privileges if needed

Performance Impact
~~~~~~~~~~~~~~~~~~

Rain CLI is designed to be lightweight:

- CPU impact: < 1%
- Memory usage: < 50MB
- Disk I/O: Minimal

Tips and Best Practices
-----------------------

1. **Use JSON mode** for scripting and automation
2. **Use live mode** for real-time monitoring
3. **Combine with other tools** like ``grep`` or ``jq`` for filtering
4. **Set up aliases** for frequently used options:

   .. code-block:: bash

      alias rainlive='rain --live'
      alias rainjson='rain --json --quiet'

5. **Monitor specific metrics** by parsing JSON output
6. **Use in dashboards** by incorporating JSON output into monitoring systems

Next Steps
----------

- Check out the :doc:`examples` for more usage scenarios
- Read the :doc:`api` for technical details
- Contribute to the project on GitHub
