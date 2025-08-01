Rain CLI Documentation
======================

Welcome to Rain CLI, a beautiful command-line tool for displaying comprehensive system information with rich formatting and colors.

.. image:: https://img.shields.io/pypi/v/rain-cli.svg
   :target: https://pypi.org/project/rain-cli/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/rain-cli.svg
   :target: https://pypi.org/project/rain-cli/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/desenyon/rain.svg
   :target: https://github.com/desenyon/rain/blob/main/LICENSE
   :alt: License

Overview
--------

Rain CLI is a modern, feature-rich system information tool that provides:

✨ **Beautiful Interface**
   Rich colors and formatting for easy reading

🔄 **Live Mode**
   Real-time system monitoring with auto-refresh

📊 **JSON Output**
   Machine-readable format for scripts and automation

🌐 **Cross-Platform**
   Works seamlessly on Linux, macOS, and Windows

⚡ **Lightweight**
   Minimal resource usage and fast execution

🔧 **Extensible**
   Modular design for easy enhancement and customization

Quick Start
-----------

Install Rain CLI using pip:

.. code-block:: bash

   pip install rain-cli

Run it to see your system information:

.. code-block:: bash

   rain

Example output::

   ╭─────────────────────────────────────────────────╮
   │                   RAIN CLI                      │
   │              System Information                 │
   ╰─────────────────────────────────────────────────╯
   
   💻 CPU: Intel(R) Core(TM) i7-9750H @ 2.60GHz
   🔧 Cores: 6 physical, 12 logical
   📊 Usage: 15.2%
   
   🧠 Memory: 8.2 GB / 16.0 GB (48.8% used)
   💾 Disk: 125.5 GB / 500.0 GB (25.1% used)

For real-time monitoring:

.. code-block:: bash

   rain --live

For machine-readable JSON output:

.. code-block:: bash

   rain --json

Key Features
------------

System Information
~~~~~~~~~~~~~~~~~~

Rain CLI displays comprehensive information about your system:

- **CPU**: Brand, cores, threads, usage, temperature
- **Memory**: Total, available, used, percentage
- **Disk**: All mounted drives with usage statistics
- **Network**: Active interfaces and IP addresses
- **OS**: Operating system, kernel, uptime

Display Modes
~~~~~~~~~~~~~

Choose from multiple display modes:

- **Default**: Beautiful colored output with icons
- **Live**: Real-time updating display
- **JSON**: Structured data for automation
- **Quiet**: Minimal output without decorations

Use Cases
---------

Rain CLI is perfect for:

- **System Administration**: Quick system health checks
- **Development**: Monitoring resources during builds
- **Automation**: JSON output for scripts and monitoring
- **Troubleshooting**: Identifying performance bottlenecks
- **Documentation**: Capturing system specifications

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   user_guide
   examples

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api
   contributing

.. toctree::
   :maxdepth: 1
   :caption: Links

   GitHub Repository <https://github.com/desenyon/rain>
   PyPI Package <https://pypi.org/project/rain-cli/>
   Issue Tracker <https://github.com/desenyon/rain/issues>

Getting Help
------------

If you encounter any issues or have questions:

1. Check the :doc:`user_guide` for common usage patterns
2. Look at the :doc:`examples` for practical use cases
3. Visit our `GitHub Issues <https://github.com/desenyon/rain/issues>`_ page
4. Read the :doc:`api` documentation for technical details

Contributing
------------

We welcome contributions! Please see our :doc:`contributing` guide for details on:

- Reporting bugs
- Suggesting features
- Submitting pull requests
- Development setup

License
-------

Rain CLI is open source software licensed under the MIT License. See the 
`LICENSE <https://github.com/desenyon/rain/blob/main/LICENSE>`_ file for details.

.. code-block:: bash

   # Show all system information
   rain

   # Show specific sections
   rain -s system -s hardware

   # Live monitoring mode
   rain --live

   # Output as JSON
   rain --json

   # Save to file
   rain --save report.txt

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
