API Reference
=============

Rain CLI provides a simple command-line interface and can also be used programmatically through its Python modules.

Command Line Interface
----------------------

Rain CLI provides a single main command with several options:

.. code-block:: bash

   rain [OPTIONS]

Options
~~~~~~~

``--live``
   Display system information in real-time with continuous updates.
   
   Example:
   
   .. code-block:: bash
   
      rain --live

``--json``
   Output system information in JSON format for machine processing.
   
   Example:
   
   .. code-block:: bash
   
      rain --json

``--quiet``
   Suppress the banner and decorative elements, showing only the essential information.
   
   Example:
   
   .. code-block:: bash
   
      rain --quiet

``--version``
   Show the version of Rain CLI and exit.
   
   Example:
   
   .. code-block:: bash
   
      rain --version

``--help``
   Show help message and exit.
   
   Example:
   
   .. code-block:: bash
   
      rain --help

JSON Output Format
------------------

When using the ``--json`` option, Rain CLI outputs structured data in the following format:

.. code-block:: json

   {
     "timestamp": "2024-01-15T14:30:25Z",
     "system": {
       "hostname": "example-host",
       "platform": "Linux",
       "platform_release": "5.4.0-42-generic",
       "platform_version": "#46-Ubuntu SMP Fri Jul 10 00:24:02 UTC 2020",
       "architecture": "x86_64",
       "processor": "x86_64"
     },
     "cpu": {
       "brand": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
       "cores": 6,
       "threads": 12,
       "usage": 15.2,
       "frequency": 2600.0,
       "temperature": 45.0
     },
     "memory": {
       "total": "16.0 GB",
       "available": "8.2 GB",
       "used": "7.8 GB",
       "usage": 48.8,
       "swap_total": "4.0 GB",
       "swap_used": "2.1 GB",
       "swap_usage": 52.5
     },
     "disks": [
       {
         "device": "/dev/sda1",
         "mountpoint": "/",
         "fstype": "ext4",
         "total": "500.0 GB",
         "free": "125.5 GB",
         "used": "374.5 GB",
         "usage": 74.9
       }
     ],
     "network": [
       {
         "interface": "eth0",
         "ip_address": "192.168.1.100",
         "netmask": "255.255.255.0",
         "broadcast": "192.168.1.255",
         "mac_address": "aa:bb:cc:dd:ee:ff"
       }
     ]
   }

Field Descriptions
~~~~~~~~~~~~~~~~~~

**System Fields**

- ``hostname``: The system hostname
- ``platform``: Operating system name (Linux, Darwin, Windows)
- ``platform_release``: OS release version
- ``platform_version``: Detailed OS version string
- ``architecture``: System architecture (x86_64, arm64, etc.)
- ``processor``: Processor architecture

**CPU Fields**

- ``brand``: CPU brand and model name
- ``cores``: Number of physical CPU cores
- ``threads``: Number of logical CPU threads
- ``usage``: Current CPU usage percentage
- ``frequency``: CPU frequency in MHz
- ``temperature``: CPU temperature in Celsius (if available)

**Memory Fields**

- ``total``: Total system RAM
- ``available``: Available RAM
- ``used``: Used RAM
- ``usage``: Memory usage percentage
- ``swap_total``: Total swap space (if configured)
- ``swap_used``: Used swap space
- ``swap_usage``: Swap usage percentage

**Disk Fields**

- ``device``: Device identifier
- ``mountpoint``: Mount point path
- ``fstype``: Filesystem type
- ``total``: Total disk capacity
- ``free``: Free disk space
- ``used``: Used disk space
- ``usage``: Disk usage percentage

**Network Fields**

- ``interface``: Network interface name
- ``ip_address``: IP address
- ``netmask``: Network mask
- ``broadcast``: Broadcast address
- ``mac_address``: MAC address

Exit Codes
----------

Rain CLI uses standard exit codes:

- ``0``: Success
- ``1``: General error
- ``2``: Command line argument error

Environment Variables
---------------------

Rain CLI respects the following environment variables:

``NO_COLOR``
   If set to any value, disables colored output.
   
   Example:
   
   .. code-block:: bash
   
      NO_COLOR=1 rain

``FORCE_COLOR``
   If set to any value, forces colored output even when not in a terminal.
   
   Example:
   
   .. code-block:: bash
   
      FORCE_COLOR=1 rain

Python Module Usage
-------------------

While Rain CLI is primarily designed as a command-line tool, its core functionality is available through Python modules.

.. note::
   
   The Python API is not currently public and may change between versions. 
   For programmatic access, it's recommended to use the JSON output format 
   with subprocess calls.

Example of programmatic usage:

.. code-block:: python

   import subprocess
   import json
   
   def get_system_info():
       """Get system information using Rain CLI"""
       result = subprocess.run(
           ['rain', '--json', '--quiet'], 
           capture_output=True, 
           text=True,
           check=True
       )
       return json.loads(result.stdout)
   
   # Usage
   info = get_system_info()
   print(f"CPU Usage: {info['cpu']['usage']:.1f}%")
   print(f"Memory Usage: {info['memory']['usage']:.1f}%")

Error Handling
--------------

Rain CLI handles errors gracefully and provides informative error messages:

Permission Errors
~~~~~~~~~~~~~~~~~

Some system information requires elevated privileges. If Rain CLI encounters permission errors, it will:

1. Skip the affected sections
2. Display available information
3. Show a warning about missing data

Missing Dependencies
~~~~~~~~~~~~~~~~~~~~

Rain CLI has optional dependencies for enhanced functionality. If these are missing:

1. Core functionality continues to work
2. Affected features are disabled
3. Fallback methods are used where possible

Network Errors
~~~~~~~~~~~~~~

For network-related information, Rain CLI handles:

1. Network interface enumeration failures
2. DNS resolution timeouts
3. Connection failures

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**"Permission denied" errors**
   Run with elevated privileges: ``sudo rain``

**Missing temperature information**
   Install hardware monitoring tools or check sensor availability

**Incomplete network information**
   Install optional dependencies: ``pip install netifaces``

**JSON parsing errors**
   Check that you're using the correct version and haven't mixed output modes

Getting Help
~~~~~~~~~~~~

For additional help:

1. Run ``rain --help`` for command-line options
2. Check the :doc:`user_guide` for detailed usage instructions
3. Visit the project's GitHub issues page for bug reports and feature requests
