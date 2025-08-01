Installation
============

Rain CLI can be installed in several ways, depending on your preference and use case.

Prerequisites
-------------

Rain CLI requires Python 3.8 or higher. You can check your Python version with:

.. code-block:: bash

   python --version

Installation Methods
--------------------

Method 1: From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install rain-cli

Method 2: From Source
~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/desenyon/rain.git
   cd rain

2. Install in development mode:

.. code-block:: bash

   pip install -e .

Method 3: Using pipx (Isolated Installation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to install Rain CLI in an isolated environment:

.. code-block:: bash

   pipx install rain-cli

Verify Installation
-------------------

After installation, verify that Rain CLI is working:

.. code-block:: bash

   rain --version

You should see output similar to::

   rain, version 1.0.0

Optional Dependencies
---------------------

Rain CLI works out of the box, but some features require additional dependencies:

Enhanced Network Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install netifaces

Detailed CPU Information
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install py-cpuinfo

GPU Information (NVIDIA)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install GPUtil

Linux Distribution Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install distro

System Requirements
-------------------

- **Python**: 3.8+
- **Operating System**: Linux, macOS, Windows
- **Memory**: Minimal (< 50MB)
- **Disk Space**: < 100MB
