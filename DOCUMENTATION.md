# Documentation Setup for SmartTree

This guide covers setting up various documentation formats for SmartTree.

## 📚 Documentation Types

### 1. Tab Completion (Shell Autocomplete)

Tab completion helps users discover options by pressing TAB. Run the provided script:

```bash
python generate_completions.py
```

This generates completion files for:
- **Bash** → `/etc/bash_completion.d/smarttree.bash`
- **Zsh** → Add to `$fpath` (e.g., `~/.zsh/completions/_smarttree`)
- **Fish** → `~/.config/fish/completions/smarttree.fish`

#### Testing Tab Completion

```bash
# After installing completions, restart shell or:
source ~/.bashrc  # for Bash

# Then test:
smarttree --[TAB]  # Should show all options
smarttree -d [TAB]  # Should suggest depth numbers
```

### 2. Man Pages (Unix Manual)

Man pages are the traditional Unix documentation accessed via `man smarttree`.

#### Building the Man Page

```bash
# The .1 extension means section 1 (user commands)
gzip -k smarttree.1  # Creates smarttree.1.gz

# Install system-wide
sudo cp smarttree.1.gz /usr/local/share/man/man1/

# Or install for current user
mkdir -p ~/.local/share/man/man1
cp smarttree.1.gz ~/.local/share/man/man1/
```

#### Testing Man Page

```bash
man smarttree  # Should display the manual
```

### 3. Info Pages (GNU Info Format)

Info pages are more detailed than man pages with hyperlinks and navigation.

#### Create smarttree.texi

```texinfo
\input texinfo
@setfilename smarttree.info
@settitle SmartTree Manual
@documentencoding UTF-8

@ifnottex
@node Top
@top SmartTree Manual

This manual is for SmartTree version 0.1.0.
@end ifnottex

@menu
* Introduction::  What is SmartTree?
* Installation::  How to install SmartTree
* Usage::         Basic usage and options
* Examples::      Common use cases
* Treeignore::    Using .treeignore files
@end menu

@node Introduction
@chapter Introduction

SmartTree is a modern directory tree viewer...

@node Installation
@chapter Installation

Install via pip:
@example
pip install smarttree
@end example

[Continue with more sections...]
```

#### Build Info Page

```bash
makeinfo smarttree.texi  # Creates smarttree.info
# Install: sudo cp smarttree.info /usr/local/share/info/
# Update dir: sudo install-info /usr/local/share/info/smarttree.info /usr/local/share/info/dir
```

### 4. Online Documentation (Recommended: MkDocs)

For a modern documentation website:

#### Setup MkDocs

```bash
pip install mkdocs mkdocs-material
```

#### Create mkdocs.yml

```yaml
site_name: SmartTree Documentation
site_url: https://development-toolbox.github.io/development-toolbox-smarttree/
repo_url: https://github.com/development-toolbox/development-toolbox-smarttree
repo_name: smarttree

theme:
  name: material
  palette:
    primary: green
    accent: light green
  features:
    - navigation.sections
    - navigation.top
    - toc.integrate
    - search.highlight
    - content.code.copy
  icon:
    logo: material/tree

nav:
  - Home: index.md
  - Installation: installation.md
  - Usage:
    - Basic Usage: usage/basic.md
    - Advanced Options: usage/advanced.md
    - Examples: usage/examples.md
  - Features:
    - Emoji Support: features/emoji.md
    - Treeignore: features/treeignore.md
    - Output Formats: features/output.md
  - API Reference: api.md
  - Contributing: contributing.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [.]

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.emoji
  - admonition
  - toc:
      permalink: true
```

#### Create Documentation Structure

```bash
mkdir -p docs/usage docs/features
# Create markdown files for each section
```

#### Build and Deploy

```bash
# Local preview
mkdocs serve  # Visit http://127.0.0.1:8000

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### 5. Package Documentation Integration

Update `pyproject.toml` to include documentation:

```toml
[project.urls]
Homepage = "https://github.com/development-toolbox/development-toolbox-smarttree"
Documentation = "https://development-toolbox.github.io/development-toolbox-smarttree/"
"Man Page" = "https://github.com/development-toolbox/development-toolbox-smarttree/blob/main/smarttree.1"
```

## 📦 Including Documentation in Package

Add to `MANIFEST.in`:

```
include README.md
include LICENSE
include smarttree.1
include completions/*
recursive-include docs *.md
```

## 🚀 Quick Setup Script

Create `setup-docs.sh`:

```bash
#!/bin/bash
# Setup all documentation for SmartTree

echo "📚 Setting up SmartTree documentation..."

# Generate completions
python generate_completions.py

# Build man page
gzip -k smarttree.1
echo "✅ Man page ready: smarttree.1.gz"

# Setup MkDocs (if needed)
if ! command -v mkdocs &> /dev/null; then
    echo "📦 Installing MkDocs..."
    pip install mkdocs mkdocs-material pymdown-extensions
fi

echo "✅ Documentation setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Install man page: sudo cp smarttree.1.gz /usr/local/share/man/man1/"
echo "2. Install completions (see generate_completions.py output)"
echo "3. Build online docs: mkdocs build"
echo "4. Deploy to GitHub Pages: mkdocs gh-deploy"
```

## 📖 Documentation Best Practices

1. **Keep README concise** - Link to full docs
2. **Update docs with code** - Document new features immediately  
3. **Include examples** - Users love copy-paste examples
4. **Add screenshots** - Especially for CLI tools
5. **Version your docs** - Tag documentation with releases

## 🎯 Priority Order

1. **README.md** ✅ (Already done)
2. **Tab completion** → Better user experience
3. **Man page** → Expected for CLI tools
4. **Online docs** → Best for detailed documentation
5. **Info pages** → Optional, less common nowadays

Would you like me to create any specific documentation file or help set up the MkDocs structure?