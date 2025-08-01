# Makefile for Rain CLI documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = docs
BUILDDIR     = docs/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Install documentation dependencies
install-docs:
	pip install -r docs/requirements.txt

# Build HTML documentation
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Build documentation and open in browser
docs: html
	@echo "Opening documentation in browser..."
	@python -c "import webbrowser; webbrowser.open('file://$(PWD)/$(BUILDDIR)/html/index.html')"

# Auto-rebuild documentation on changes
auto:
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" --host 0.0.0.0 --port 8000

# Clean built documentation
clean:
	rm -rf "$(BUILDDIR)"

# Check for broken links
linkcheck:
	@$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS) $(O)

# Build PDF documentation
pdf:
	@$(SPHINXBUILD) -b pdf "$(SOURCEDIR)" "$(BUILDDIR)/pdf" $(SPHINXOPTS) $(O)

# Build EPUB documentation
epub:
	@$(SPHINXBUILD) -b epub "$(SOURCEDIR)" "$(BUILDDIR)/epub" $(SPHINXOPTS) $(O)

# Run all tests
test:
	python tests.py

# Format code
format:
	black .
	isort .

# Lint code
lint:
	flake8 .
	pylint core/ cli/ utils/

# Type check
typecheck:
	mypy core/ cli/ utils/

# Full quality check
quality: format lint typecheck test

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
