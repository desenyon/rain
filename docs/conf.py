# Configuration file for the Sphinx documentation builder.

project = 'Rain CLI'
copyright = '2024, Desenyon'
author = 'Desenyon'
release = '1.0.0'

# Extensions
extensions = [
    'myst_parser',
    'sphinx_copybutton',
]

# Source file extensions
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# The master toctree document
master_doc = 'index'

# HTML theme options
html_theme = 'furo'
html_title = f"{project} Documentation"
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}

# MyST parser options
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

# Copy button options
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
