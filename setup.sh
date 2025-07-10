#!/bin/bash
# setup.sh - Quick setup script for SmartTree documentation and development

set -e  # Exit on error

echo "🌳 SmartTree Setup Script"
echo "========================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print colored output
print_success() {
    echo -e "\033[32m✅ $1\033[0m"
}

print_error() {
    echo -e "\033[31m❌ $1\033[0m"
}

print_info() {
    echo -e "\033[34mℹ️  $1\033[0m"
}

# Step 1: Generate shell completions
echo "📝 Generating shell completions..."
if python generate_completions.py; then
    print_success "Shell completions generated"
else
    print_error "Failed to generate completions"
    exit 1
fi

# Step 2: Build man page
echo ""
echo "📄 Building man page..."
if [ -f "smarttree.1" ]; then
    gzip -kf smarttree.1
    print_success "Man page built: smarttree.1.gz"
else
    print_error "smarttree.1 not found"
    exit 1
fi

# Step 3: Create directories for local installation
echo ""
echo "📁 Creating local directories..."
mkdir -p ~/.local/share/man/man1
mkdir -p ~/.local/share/bash-completion/completions
mkdir -p ~/.config/fish/completions
mkdir -p ~/.zsh/completions
print_success "Local directories created"

# Step 4: Install documentation locally (optional)
echo ""
read -p "📦 Install documentation locally for current user? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Install man page
    cp smarttree.1.gz ~/.local/share/man/man1/
    print_success "Man page installed"
    
    # Install completions based on current shell
    if [ -n "$BASH_VERSION" ]; then
        cp completions/smarttree.bash ~/.local/share/bash-completion/completions/
        print_success "Bash completions installed"
    fi
    
    if [ -n "$ZSH_VERSION" ]; then
        cp completions/_smarttree ~/.zsh/completions/
        print_success "Zsh completions installed"
        print_info "Add to ~/.zshrc: fpath=(~/.zsh/completions \$fpath)"
    fi
    
    if command_exists fish; then
        cp completions/smarttree.fish ~/.config/fish/completions/
        print_success "Fish completions installed"
    fi
    
    print_info "Restart your shell or run: source ~/.bashrc"
fi

# Step 5: Check Python packaging tools
echo ""
echo "🔧 Checking Python packaging tools..."
if command_exists pip; then
    if ! pip show build >/dev/null 2>&1; then
        print_info "Installing 'build' package..."
        pip install --user build
    fi
    if ! pip show twine >/dev/null 2>&1; then
        print_info "Installing 'twine' package..."
        pip install --user twine
    fi
    print_success "Python packaging tools ready"
else
    print_error "pip not found. Please install Python and pip."
fi

# Step 6: Create distribution files (optional)
echo ""
read -p "📦 Build distribution packages for PyPI? [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Cleaning old distributions..."
    rm -rf dist/ build/ *.egg-info
    
    print_info "Building distribution packages..."
    if python -m build; then
        print_success "Distribution packages built in dist/"
        echo ""
        echo "📤 To upload to PyPI, run:"
        echo "   python -m twine upload dist/*"
    else
        print_error "Failed to build distribution"
    fi
fi

# Step 7: Summary
echo ""
echo "📊 Setup Summary"
echo "================"
echo ""
print_success "Documentation generated:"
echo "  • Shell completions in completions/"
echo "  • Man page: smarttree.1.gz"
echo ""

if [ -d "dist" ]; then
    print_success "Distribution packages ready in dist/"
    echo ""
fi

echo "📚 Next Steps:"
echo "1. Test locally: pip install -e ."
echo "2. Test the command: smarttree --help"
echo "3. Commit changes: git add . && git commit"
echo "4. Upload to PyPI: python -m twine upload dist/*"
echo ""

echo "📖 Documentation Commands:"
echo "  man smarttree         # View man page (after install)"
echo "  smarttree --[TAB]     # Test tab completion"
echo "  make docs-serve       # Start local docs server (if using MkDocs)"
echo ""

print_success "Setup complete! 🎉"