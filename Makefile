# Makefile for SmartTree documentation

.PHONY: all clean completions man install-local install-system docs

all: completions man

# Generate shell completion scripts
completions:
	@echo "🔧 Generating shell completions..."
	@python generate_completions.py

# Build man page
man: smarttree.1
	@echo "📄 Building man page..."
	@gzip -kf smarttree.1
	@echo "✅ Built smarttree.1.gz"

# Install for current user only
install-local: completions man
	@echo "📦 Installing locally for current user..."
	@mkdir -p ~/.local/share/man/man1
	@cp smarttree.1.gz ~/.local/share/man/man1/
	@mkdir -p ~/.local/share/bash-completion/completions
	@cp completions/smarttree.bash ~/.local/share/bash-completion/completions/
	@echo "✅ Installed locally. Restart your shell or run: source ~/.bashrc"

# Install system-wide (requires sudo)
install-system: completions man
	@echo "📦 Installing system-wide (requires sudo)..."
	sudo cp smarttree.1.gz /usr/local/share/man/man1/
	sudo cp completions/smarttree.bash /etc/bash_completion.d/
	@echo "✅ Installed system-wide"

# Build online documentation (requires mkdocs)
docs:
	@echo "📚 Building online documentation..."
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs build; \
		echo "✅ Documentation built in site/"; \
	else \
		echo "❌ MkDocs not installed. Run: pip install mkdocs mkdocs-material"; \
	fi

# Serve documentation locally
docs-serve:
	@echo "🌐 Starting local documentation server..."
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs serve; \
	else \
		echo "❌ MkDocs not installed. Run: pip install mkdocs mkdocs-material"; \
	fi

# Deploy documentation to GitHub Pages
docs-deploy:
	@echo "🚀 Deploying documentation to GitHub Pages..."
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs gh-deploy; \
	else \
		echo "❌ MkDocs not installed. Run: pip install mkdocs mkdocs-material"; \
	fi

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f smarttree.1.gz
	@rm -rf completions/
	@rm -rf site/
	@rm -rf __pycache__/
	@rm -f *.pyc
	@echo "✅ Cleaned"

# Display help
help:
	@echo "SmartTree Documentation Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make              - Build completions and man page"
	@echo "  make completions  - Generate shell completion scripts"
	@echo "  make man          - Build man page"
	@echo "  make install-local - Install for current user"
	@echo "  make install-system - Install system-wide (needs sudo)"
	@echo "  make docs         - Build online documentation"
	@echo "  make docs-serve   - Serve docs locally at http://localhost:8000"
	@echo "  make docs-deploy  - Deploy docs to GitHub Pages"
	@echo "  make clean        - Remove generated files"
	@echo "  make help         - Show this help message"