# Configuration file for the Sphinx documentation builder.

project = 'Rain CLI'
copyright = '2024, Desenyon'
author = 'Desenyon'
release = '1.0.0'

# Extensions - minimal set for RST only
extensions = [
    'sphinx_copybutton',
]

# The master toctree document
master_doc = 'index'

# HTML theme options
html_theme = 'furo'
html_title = f"{project} Documentation"
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}

# Copy button options
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
