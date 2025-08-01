Contributing
============

Thank you for your interest in contributing to Rain CLI! This document provides guidelines and information for contributors.

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork and Clone**

   Fork the repository on GitHub and clone your fork:

   .. code-block:: bash

      git clone https://github.com/yourusername/rain.git
      cd rain

2. **Set up Development Environment**

   Create a virtual environment and install dependencies:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -e .
      pip install -r requirements-dev.txt

3. **Install Optional Dependencies**

   For full functionality during development:

   .. code-block:: bash

      pip install netifaces distro GPUtil py-cpuinfo

4. **Verify Installation**

   Test that everything works:

   .. code-block:: bash

      rain --version
      python -m pytest

Project Structure
-----------------

Understanding the codebase:

.. code-block:: text

   rain/
   ├── cli/
   │   └── main.py          # Main CLI entry point
   ├── core/
   │   ├── collector.py     # System information collection
   │   └── robust_collector.py  # Robust collection with fallbacks
   ├── tests/
   │   └── test_*.py        # Test files
   ├── docs/
   │   ├── conf.py          # Sphinx configuration
   │   └── *.rst            # Documentation files
   ├── setup.py             # Package setup
   └── README.md            # Project readme

Key Components
~~~~~~~~~~~~~~

**CLI Module (``cli/main.py``)**
   - Command-line interface implementation
   - Argument parsing and validation
   - Output formatting and display

**Core Module (``core/collector.py``)**
   - System information collection
   - Cross-platform compatibility
   - Performance optimization

**Robust Collector (``core/robust_collector.py``)**
   - Error-resistant collection methods
   - Graceful degradation
   - Fallback implementations

How to Contribute
-----------------

Types of Contributions
~~~~~~~~~~~~~~~~~~~~~~

We welcome various types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Implement features or fix bugs
- **Documentation**: Improve or expand documentation
- **Testing**: Add test coverage or improve existing tests

Reporting Bugs
~~~~~~~~~~~~~~

When reporting bugs, please include:

1. **Environment Information**:
   - Operating system and version
   - Python version
   - Rain CLI version
   - Output of ``rain --json`` (if relevant)

2. **Steps to Reproduce**:
   - Exact commands that trigger the issue
   - Expected vs. actual behavior
   - Any error messages

3. **Additional Context**:
   - Screenshots (if applicable)
   - System specifications
   - Other relevant software versions

**Bug Report Template**:

.. code-block:: text

   **Environment**
   - OS: [e.g., Ubuntu 20.04, macOS 12.0, Windows 10]
   - Python: [e.g., 3.9.7]
   - Rain CLI: [e.g., 1.0.0]

   **Description**
   A clear description of the bug.

   **Steps to Reproduce**
   1. Run `rain ...`
   2. See error

   **Expected Behavior**
   What you expected to happen.

   **Actual Behavior**
   What actually happened.

   **Additional Context**
   Any other relevant information.

Suggesting Features
~~~~~~~~~~~~~~~~~~~

For feature requests, please:

1. **Check Existing Issues**: Ensure the feature hasn't been requested
2. **Describe the Use Case**: Explain why this feature would be useful
3. **Propose Implementation**: If you have ideas on how to implement it
4. **Consider Scope**: Keep features focused and maintainable

**Feature Request Template**:

.. code-block:: text

   **Feature Description**
   A clear description of the proposed feature.

   **Use Case**
   Why would this feature be useful? What problem does it solve?

   **Proposed Implementation**
   If you have ideas on how to implement this feature.

   **Alternatives Considered**
   Other approaches you've considered.

Code Contributions
~~~~~~~~~~~~~~~~~~

Development Workflow
^^^^^^^^^^^^^^^^^^^^^

1. **Create an Issue**: Discuss your changes before implementing
2. **Create a Branch**: Use descriptive branch names
3. **Make Changes**: Follow coding standards and test your changes
4. **Submit a Pull Request**: Include a clear description

**Branch Naming**:

- ``feature/description`` for new features
- ``fix/description`` for bug fixes
- ``docs/description`` for documentation changes

**Commit Messages**:

Use clear, descriptive commit messages:

.. code-block:: text

   Add CPU temperature monitoring for Linux

   - Implement temperature collection using /sys/class/thermal
   - Add fallback for systems without thermal sensors
   - Update tests for new functionality

   Closes #123

Coding Standards
^^^^^^^^^^^^^^^^

**Python Style**:

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

**Code Quality**:

- Run tests before submitting: ``python -m pytest``
- Check code style: ``flake8``
- Ensure type correctness: ``mypy`` (if configured)

**Example Function**:

.. code-block:: python

   def get_cpu_temperature() -> Optional[float]:
       """Get CPU temperature in Celsius.
       
       Returns:
           CPU temperature in Celsius, or None if unavailable.
           
       Raises:
           OSError: If temperature sensors are not accessible.
       """
       try:
           with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
               temp_millidegrees = int(f.read().strip())
               return temp_millidegrees / 1000.0
       except (FileNotFoundError, PermissionError, ValueError):
           return None

Testing
^^^^^^^

**Writing Tests**:

- Add tests for new functionality
- Test edge cases and error conditions
- Use meaningful test names
- Mock external dependencies

**Test Categories**:

- **Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **Platform Tests**: Test cross-platform compatibility

**Example Test**:

.. code-block:: python

   def test_get_cpu_temperature_success():
       """Test successful CPU temperature retrieval."""
       with patch('builtins.open', mock_open(read_data='45000')):
           temp = get_cpu_temperature()
           assert temp == 45.0

   def test_get_cpu_temperature_file_not_found():
       """Test handling of missing temperature file."""
       with patch('builtins.open', side_effect=FileNotFoundError):
           temp = get_cpu_temperature()
           assert temp is None

Documentation
~~~~~~~~~~~~~

**Documentation Types**:

- **User Documentation**: How to use Rain CLI
- **Developer Documentation**: How to contribute and extend
- **API Documentation**: Function and module references

**Writing Guidelines**:

- Use clear, concise language
- Include practical examples
- Keep documentation up-to-date with code changes
- Test documentation examples

**Building Documentation**:

.. code-block:: bash

   cd docs
   sphinx-build -b html . _build/html

Pull Request Process
--------------------

Submission Guidelines
~~~~~~~~~~~~~~~~~~~~~

1. **Pre-submission Checklist**:
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Documentation is updated
   - [ ] Commit messages are clear
   - [ ] Branch is up-to-date with main

2. **Pull Request Description**:
   - Clear title summarizing changes
   - Detailed description of what changed
   - Reference related issues
   - Include testing notes

**Pull Request Template**:

.. code-block:: text

   ## Description
   Brief description of changes.

   ## Changes Made
   - List of specific changes
   - Another change

   ## Testing
   - How the changes were tested
   - Any manual testing performed

   ## Related Issues
   Closes #123

   ## Screenshots (if applicable)
   [Include screenshots for UI changes]

Review Process
~~~~~~~~~~~~~~

1. **Automated Checks**: CI/CD runs tests and checks
2. **Code Review**: Maintainers review code quality and design
3. **Testing**: Changes are tested on different platforms
4. **Merge**: Approved changes are merged to main branch

**Review Criteria**:

- Code quality and style
- Test coverage
- Documentation completeness
- Performance impact
- Cross-platform compatibility

Release Process
---------------

Rain CLI follows semantic versioning (SemVer):

- **Major (x.0.0)**: Breaking changes
- **Minor (0.x.0)**: New features, backward compatible
- **Patch (0.0.x)**: Bug fixes, backward compatible

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

We are committed to providing a welcoming and inclusive environment:

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together constructively
- **Be Patient**: Help others learn and grow
- **Be Inclusive**: Welcome diverse perspectives and backgrounds

Communication
~~~~~~~~~~~~~

- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code discussions and reviews
- **Discussions**: General questions and community support

Recognition
~~~~~~~~~~~

Contributors are recognized in:

- ``CONTRIBUTORS.md`` file
- Release notes
- Project documentation

Getting Help
------------

If you need help contributing:

1. **Check Documentation**: Start with this guide and user documentation
2. **Search Issues**: Look for similar questions or problems
3. **Ask Questions**: Open a discussion or issue for help
4. **Contact Maintainers**: Reach out directly if needed

**Useful Resources**:

- `GitHub Flow Guide <https://guides.github.com/introduction/flow/>`_
- `Python Style Guide (PEP 8) <https://www.python.org/dev/peps/pep-0008/>`_
- `Sphinx Documentation <https://www.sphinx-doc.org/>`_

Thank you for contributing to Rain CLI! Your help makes this project better for everyone.
