#!/usr/bin/env python3
"""
smarttree - Smart Directory Tree Viewer

SmartTree is a modern, cross-platform CLI tool to visualize directory structures 
like the Unix tree command — with enhanced features such as emoji support, 
Markdown export, colorized output, depth control, .treeignore filtering, and 
summary statistics. Built with Python, ideal for automation, documentation, 
and DevOps workflows.

Author: Johan Sörell
GitHub: https://github.com/development-toolbox/development-toolbox-smarttree
Blog:   https://automationblueprint.site
License: MIT

Features:
- Tree view of folders/files
- Depth limit (--depth)
- Color folder names (--color)
- Output to .txt / .md (--output)
- Emoji icons in Markdown (--emoji / --no-emoji)
- Summary of total files/folders (--summary)
- .treeignore file support (like .gitignore)
- Log to plain text file (--log)

Installation:
    pip install smarttree

Usage:
    smarttree
    smarttree /path/to/directory
    smarttree --depth 2 --emoji --output tree.md
"""

import os
import argparse
import sys
import io
from typing import cast, TextIO

__version__ = "0.1.0"
__author__ = "Johan Sörell"

# Fix for Pylance false positive on .reconfigure() (Python 3.7+)
stdout = cast(TextIO, sys.stdout)
if hasattr(stdout, "reconfigure"):
    stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

def load_treeignore(base_path):
    """Load ignore patterns from .treeignore file."""
    ignore_file = os.path.join(base_path, ".treeignore")
    ignore_set = set()
    if os.path.exists(ignore_file):
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_set.add(line)
    return ignore_set

def colorize(text, is_dir, use_color):
    """Apply color to directory names if enabled."""
    if use_color and is_dir:
        return f"\033[94m{text}\033[0m"
    return str(text)

def print_tree(startpath, prefix="", level=0, max_depth=None,
               use_color=False, output_lines=None, stats=None,
               ignore_set=None, emoji=False):
    """Recursively print directory tree structure."""
    try:
        items = sorted(os.listdir(startpath))
    except Exception as e:
        print(f"❌ Cannot access {startpath}: {e}", file=sys.stderr)
        return

    for idx, item in enumerate(items):
        if item in ignore_set:
            continue

        path = os.path.join(startpath, item)
        is_dir = os.path.isdir(path)
        connector = "└── " if idx == len(items) - 1 else "├── "

        emoji_icon = ""
        if emoji and output_lines is not None:
            emoji_icon = "📁 " if is_dir else "📄 "

        raw_line = prefix + connector + item
        terminal_line = prefix + connector + colorize(item, is_dir, use_color)
        markdown_line = prefix + connector + emoji_icon + item

        print(terminal_line)

        if output_lines is not None:
            output_lines.append(markdown_line)

        if stats is not None:
            stats["dirs" if is_dir else "files"] += 1

        if is_dir:
            if max_depth is None or level + 1 < max_depth:
                extension = "    " if idx == len(items) - 1 else "│   "
                print_tree(path, prefix + extension, level + 1,
                           max_depth, use_color, output_lines, stats,
                           ignore_set, emoji)

def main():
    """Main entry point for smarttree command."""
    parser = argparse.ArgumentParser(
        prog="smarttree",
        description="🌳 SmartTree - Modern cross-platform directory tree viewer with emoji support, Markdown export, .treeignore filtering, and colorized output",
        epilog="""Examples:
  smarttree
  smarttree /var/log -d 2
  smarttree -o tree.md -d 3 --summary --emoji
  smarttree --color --log run.log

Markdown Output:
  If --output ends with '.md', output is wrapped in a fenced code block.
  Emoji icons are enabled by default for Markdown unless --no-emoji is set.

Ignore Patterns:
  If a .treeignore file exists in the target folder, matching entries will be excluded.

Project:
  GitHub: https://github.com/development-toolbox/development-toolbox-smarttree
  Author: Johan Sörell
  Blog:   https://automationblueprint.site
""",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory path to scan (default: current directory)"
    )
    parser.add_argument("-d", "--depth", type=int, help="Limit recursion depth (like 'tree -L N')")
    parser.add_argument("-o", "--output", help="Output file (e.g. 'tree.txt' or 'tree.md')")
    parser.add_argument("-c", "--color", action="store_true", help="Enable color for folders (blue)")
    parser.add_argument("-s", "--summary", action="store_true", help="Show total file and folder count after listing")
    parser.add_argument("--log", help="Save output to an additional .log file (plain text)")
    parser.add_argument("--emoji", dest="emoji", action="store_true", help="Enable emoji icons (📁, 📄) in Markdown output")
    parser.add_argument("--no-emoji", dest="emoji", action="store_false", help="Disable emoji icons (📁, 📄)")
    parser.add_argument("-v", "--version", action="version", version=f"smarttree {__version__}")
    parser.set_defaults(emoji=None)

    args = parser.parse_args()

    abs_path = os.path.abspath(args.path)
    print(f"📂 {abs_path}")

    output_lines = [] if args.output or args.log else None
    stats = {"dirs": 0, "files": 0} if args.summary else None
    ignore_set = load_treeignore(args.path)

    # emoji default logic: auto-on if Markdown and not explicitly disabled
    use_emoji = args.emoji if args.emoji is not None else (
        args.output.endswith(".md") if args.output else False
    )

    print_tree(
        args.path,
        max_depth=args.depth,
        use_color=args.color,
        output_lines=output_lines,
        stats=stats,
        ignore_set=ignore_set,
        emoji=use_emoji,
    )

    if args.summary and stats:
        print("\n📊 Summary:")
        print(f"  📁 Folders: {stats['dirs']}")
        print(f"  📄 Files:   {stats['files']}")

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                if args.output and args.output.endswith(".md"):
                    f.write(f"```\n📂 {abs_path}\n")
                    if output_lines:
                        f.write("\n".join(str(line) for line in output_lines))
                    f.write("\n```\n")
                else:
                    f.write(f"{abs_path}\n")
                    if output_lines:
                        f.write("\n".join(str(line) for line in output_lines))
            print(f"\n✅ Output saved to: {args.output}")
        except Exception as e:
            print(f"❌ Failed to write output: {e}", file=sys.stderr)

    if args.log:
        try:
            with open(args.log, "w", encoding="utf-8") as logf:
                logf.write(f"{abs_path}\n")
                if output_lines:
                    logf.write("\n".join(str(line) for line in output_lines))
                else:
                    logf.write("[No output generated]\n")
            print(f"📄 Log saved to: {args.log}")
        except Exception as e:
            print(f"❌ Failed to write log: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()