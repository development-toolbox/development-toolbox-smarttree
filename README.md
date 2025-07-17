# 🌳 smarttree

[![PyPI version](https://badge.fury.io/py/smarttree.svg)](https://badge.fury.io/py/smarttree)
[![Python Support](https://img.shields.io/pypi/pyversions/smarttree.svg)](https://pypi.org/project/smarttree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SmartTree is a modern, cross-platform CLI tool to visualize directory structures like the Unix tree command — with enhanced features such as emoji support, Markdown export, colorized output, depth control, .treeignore filtering, and summary statistics. Built with Python, ideal for automation, documentation, and DevOps workflows.

## ✨ Features

- 📁 **Tree visualization** - Display directory structure in a tree format
- 🎨 **Colored output** - Optionally colorize folders for better visibility
- 📊 **Depth control** - Limit tree depth with `--depth` flag
- 📝 **Multiple output formats** - Export to text or markdown files
- 😊 **Emoji support** - Add visual indicators for files and folders
- 🚫 **Smart ignore** - Advanced `.treeignore` with wildcard patterns like `.gitignore`
- 📈 **Statistics** - Show summary of total files and folders
- 📜 **Logging** - Save output to log files for documentation

## 🚀 Installation

```bash
pip install smarttree
```

## 🆕 What's New in v0.2.0

- **Enhanced `.treeignore`** - Now supports full wildcard patterns (`*`, `?`, `[seq]`)
- **Directory-specific patterns** - Use trailing `/` to match only directories
- **Better pattern matching** - Works like `.gitignore` with `fnmatch` patterns
- **Case-sensitive matching** - Consistent behavior across all platforms
- **Comprehensive documentation** - Added man pages and shell completions

## 📖 Usage

### Basic usage

```bash
# Display tree of current directory
smarttree

# Display tree of specific directory
smarttree /path/to/directory
```

### Common options

```bash
# Limit depth to 2 levels
smarttree --depth 2

# Enable colored output
smarttree --color

# Show summary statistics
smarttree --summary

# Export to markdown with emojis
smarttree --output tree.md --emoji

# Combine multiple options
smarttree ~/projects --depth 3 --color --summary --output project-tree.md
```

### All options

```
usage: smarttree [-h] [-d DEPTH] [-o OUTPUT] [-c] [-s] [--log LOG] [--emoji] [--no-emoji] [-v] [path]

🌳 SmartTree - Modern cross-platform directory tree viewer with emoji support, Markdown export, .treeignore filtering, and colorized output

positional arguments:
  path                  Directory path to scan (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        Limit recursion depth (like 'tree -L N')
  -o OUTPUT, --output OUTPUT
                        Output file (e.g. 'tree.txt' or 'tree.md')
  -c, --color           Enable color for folders (blue)
  -s, --summary         Show total file and folder count after listing
  --log LOG             Save output to an additional .log file (plain text)
  --emoji               Enable emoji icons (📁, 📄) in Markdown output
  --no-emoji            Disable emoji icons (📁, 📄)
  -v, --version         show program's version number and exit
```

## 🚫 Using .treeignore

Create a `.treeignore` file in any directory to exclude specific files or folders from the tree output. The syntax supports wildcards and patterns similar to `.gitignore`:

```bash
# .treeignore example

# Ignore specific files
.DS_Store
Thumbs.db
*.log

# Ignore file patterns
*.pyc
*.pyo
*.swp
*~

# Ignore directories (trailing slash)
__pycache__/
.git/
node_modules/
.venv/
venv/
env/

# Ignore by wildcard patterns
build*/
dist*/
*.egg-info/
.*.cache/

# Comments start with #
# Each pattern is matched against filenames using fnmatch
```

### Pattern Rules:
- `*` matches any number of characters
- `?` matches a single character
- `[seq]` matches any character in seq
- `[!seq]` matches any character not in seq
- Patterns ending with `/` only match directories
- Patterns without `/` match both files and directories
- **Pattern matching is case-sensitive** (e.g., `*.PNG` won't match `file.png`)
- **Pattern matching is case-sensitive** (e.g., `*.PNG` won't match `file.png`)

## 📸 Examples

### Basic tree output
```
📂 /home/user/my-project
├── 📁 src
│   ├── 📄 main.py
│   └── 📄 utils.py
├── 📁 tests
│   └── 📄 test_main.py
├── 📄 README.md
└── 📄 setup.py
```

### With summary
```
📂 /home/user/my-project
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── README.md
└── setup.py

📊 Summary:
  📁 Folders: 2
  📄 Files:   5
```

### Markdown output
When using `--output file.md`, the tree is automatically wrapped in a code block:

````markdown
```
📂 /home/user/my-project
├── 📁 src
│   ├── 📄 main.py
│   └── 📄 utils.py
...
```
````

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/development-toolbox/development-toolbox-smarttree.git
cd development-toolbox-smarttree

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Johan Sörell**

- GitHub: [@J-SirL](https://github.com/J-SirL)
- Blog: [automationblueprint.site](https://automationblueprint.site)

## 🙏 Acknowledgments

- Inspired by the Unix `tree` command
- Built with Python's standard library - no external dependencies required
- Special thanks to all contributors

---

If you find this tool useful, please consider giving it a ⭐ on GitHub!