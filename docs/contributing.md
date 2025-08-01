# Contributing

Thank you for your interest in contributing to Rain CLI! This guide will help you get started with contributing to the project.

## Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/rain.git
   cd rain
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e .
   pip install -r docs/requirements.txt
   ```

4. **Run Tests**
   ```bash
   python tests.py
   ```

### Project Structure

```
rain/
├── cli/                 # Command-line interface
│   └── main.py         # Main CLI entry point
├── core/               # Core functionality
│   ├── collector.py    # System information collection
│   ├── robust_collector.py  # Robust collector with fallbacks
│   ├── display.py      # Display management
│   └── config.py       # Configuration management
├── utils/              # Utility modules
│   ├── exceptions.py   # Custom exceptions
│   ├── logger.py       # Logging utilities
│   └── helpers.py      # Helper functions
├── docs/               # Documentation
├── tests.py           # Test suite
├── requirements.txt   # Dependencies
└── README.md          # Project README
```

## Development Guidelines

### Code Style

We follow PEP 8 with some specific guidelines:

- **Line Length**: 88 characters (Black formatter standard)
- **Imports**: Use absolute imports, group imports logically
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Use type hints for all public functions

Example:
```python
def collect_system_info(self, include_env: bool = False) -> Dict[str, Any]:
    """
    Collect basic system information.
    
    Args:
        include_env: Whether to include environment variables
        
    Returns:
        Dictionary containing system information
        
    Raises:
        CollectionError: If system information cannot be collected
    """
```

### Error Handling

- Use custom exceptions from `utils.exceptions`
- Provide graceful fallbacks for missing dependencies
- Log errors appropriately
- Never crash on missing optional features

Example:
```python
try:
    import optional_library
    data = optional_library.get_data()
except ImportError:
    logger.warning("Optional library not available, using fallback")
    data = fallback_implementation()
except Exception as e:
    logger.error(f"Failed to collect data: {e}")
    data = {}
```

### Testing

- Write tests for new features
- Maintain existing test coverage
- Use descriptive test names
- Test error conditions and edge cases

Example:
```python
def test_collect_system_info_handles_missing_dependency(self):
    """Test that system info collection handles missing dependencies gracefully."""
    with patch('core.collector.optional_import', return_value=None):
        collector = SystemCollector()
        result = collector.collect_system_info()
        self.assertIsInstance(result, dict)
        self.assertIn('os', result)
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   ```bash
   rain --version
   python --version
   # OS and version
   ```

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Error messages or stack traces

3. **Minimal Example**
   - Simplest command that reproduces the issue
   - Relevant configuration if applicable

### Feature Requests

For new features, please provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Examples**: How would users interact with this feature?

### Code Contributions

#### Adding New System Information

To add a new type of system information:

1. **Add Collection Method**
   ```python
   def collect_new_info(self) -> Dict[str, Any]:
       """Collect new system information."""
       try:
           # Collection logic here
           return {"new_data": data}
       except Exception as e:
           raise CollectionError(f"Failed to collect new info: {e}")
   ```

2. **Add Display Method**
   ```python
   def _display_new_info(self, data: Dict[str, Any]) -> None:
       """Display new information."""
       # Rich formatting logic here
   ```

3. **Update Section Mapping**
   ```python
   section_collectors = {
       # ... existing sections
       "new_section": self.collect_new_info,
   }
   ```

4. **Add Tests**
   ```python
   def test_collect_new_info(self):
       """Test new info collection."""
       collector = RobustSystemCollector()
       result = collector.collect_new_info()
       self.assertIsInstance(result, dict)
       self.assertIn('new_data', result)
   ```

#### Adding New Display Options

To add new display formatting:

1. **Add Display Method**
2. **Update CLI Options** if needed
3. **Add Configuration Options** if applicable
4. **Test Different Scenarios**

#### Improving Cross-Platform Support

- Test on multiple operating systems
- Use `platform.system()` for OS-specific code
- Provide graceful fallbacks
- Document platform-specific features

## Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   python tests.py
   rain --version  # Test CLI works
   ```

2. **Update Documentation**
   - Update docstrings
   - Add/update relevant documentation
   - Update changelog if applicable

3. **Check Code Style**
   ```bash
   # Optional: Use black formatter
   pip install black
   black .
   ```

### Submitting

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   # or
   git checkout -b fix/bug-description
   ```

2. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add new feature: description"
   ```

3. **Push and Create PR**
   ```bash
   git push origin feature/new-feature
   ```

### PR Template

Please include:

- **Description**: What does this PR do?
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How was this tested?
- **Screenshots**: If applicable
- **Checklist**: 
  - [ ] Tests pass
  - [ ] Documentation updated
  - [ ] No breaking changes (or documented)

## Development Tips

### Testing Locally

```bash
# Run specific test
python -m unittest tests.TestSystemCollector.test_collect_system_info

# Test CLI functionality
python rain.py -s system --no-banner

# Test JSON output
python rain.py --json -s system | jq .
```

### Debugging

```bash
# Enable verbose logging
python rain.py -v -s system

# Debug specific module
python -c "
from core.robust_collector import RobustSystemCollector
collector = RobustSystemCollector()
data = collector.collect_system_info()
print(data)
"
```

### Documentation

```bash
# Build documentation locally
cd docs
sphinx-build -b html . _build/html

# Auto-rebuild on changes
sphinx-autobuild . _build/html
```

## Code Review Guidelines

### For Contributors

- Keep PRs focused and small
- Write clear commit messages
- Respond to feedback promptly
- Test on multiple platforms if possible

### For Reviewers

- Be constructive and helpful
- Focus on code quality and maintainability
- Consider backward compatibility
- Test the changes if possible

## Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Changelog

Update `CHANGELOG.md` with:
- New features
- Bug fixes
- Breaking changes
- Deprecations

## Getting Help

- **Discussions**: GitHub Discussions for questions
- **Issues**: GitHub Issues for bugs and features
- **Documentation**: Read the Docs for user guides
- **Code**: Inline comments and docstrings

## Recognition

All contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Documentation credits

Thank you for contributing to Rain CLI! 🌧️
