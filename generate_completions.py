#!/usr/bin/env python3
"""
Generate shell completion scripts for smarttree
"""

import os
import sys

def generate_bash_completion():
    """Generate Bash completion script"""
    return '''# bash completion for smarttree
_smarttree() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="-h --help -d --depth -o --output -c --color -s --summary --log --emoji --no-emoji -v --version"

    # Handle option arguments
    case "${prev}" in
        -d|--depth)
            COMPREPLY=( $(compgen -W "1 2 3 4 5" -- ${cur}) )
            return 0
            ;;
        -o|--output|--log)
            COMPREPLY=( $(compgen -f -- ${cur}) )
            return 0
            ;;
    esac

    # Handle options
    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    # Default to directory completion
    COMPREPLY=( $(compgen -d -- ${cur}) )
}

complete -F _smarttree smarttree
'''

def generate_zsh_completion():
    """Generate Zsh completion script"""
    return '''#compdef smarttree

_smarttree() {
    local -a opts
    opts=(
        '(-h --help)'{-h,--help}'[Show help message and exit]'
        '(-d --depth)'{-d,--depth}'[Limit recursion depth]:depth:_numbers'
        '(-o --output)'{-o,--output}'[Output file]:output file:_files'
        '(-c --color)'{-c,--color}'[Enable color for folders]'
        '(-s --summary)'{-s,--summary}'[Show total file and folder count]'
        '--log[Save output to log file]:log file:_files'
        '--emoji[Enable emoji icons in output]'
        '--no-emoji[Disable emoji icons]'
        '(-v --version)'{-v,--version}'[Show version number and exit]'
        '*:directory:_directories'
    )

    _arguments -s $opts
}

_smarttree "$@"
'''

def generate_fish_completion():
    """Generate Fish completion script"""
    return '''# Fish completion for smarttree
complete -c smarttree -s h -l help -d "Show help message and exit"
complete -c smarttree -s d -l depth -x -d "Limit recursion depth"
complete -c smarttree -s o -l output -r -d "Output file"
complete -c smarttree -s c -l color -d "Enable color for folders"
complete -c smarttree -s s -l summary -d "Show total file and folder count"
complete -c smarttree -l log -r -d "Save output to log file"
complete -c smarttree -l emoji -d "Enable emoji icons"
complete -c smarttree -l no-emoji -d "Disable emoji icons"
complete -c smarttree -s v -l version -d "Show version number and exit"

# Complete directories for positional argument
complete -c smarttree -a "(__fish_complete_directories)"
'''

def main():
    """Generate completion files for all shells"""
    
    completions_dir = "completions"
    os.makedirs(completions_dir, exist_ok=True)
    
    # Generate Bash completion
    with open(os.path.join(completions_dir, "smarttree.bash"), "w") as f:
        f.write(generate_bash_completion())
    print("✅ Generated completions/smarttree.bash")
    
    # Generate Zsh completion
    with open(os.path.join(completions_dir, "_smarttree"), "w") as f:
        f.write(generate_zsh_completion())
    print("✅ Generated completions/_smarttree (Zsh)")
    
    # Generate Fish completion
    with open(os.path.join(completions_dir, "smarttree.fish"), "w") as f:
        f.write(generate_fish_completion())
    print("✅ Generated completions/smarttree.fish")
    
    print("\n📝 Installation instructions:")
    print("\nBash:")
    print("  sudo cp completions/smarttree.bash /etc/bash_completion.d/")
    print("  # Or for user only:")
    print("  cp completions/smarttree.bash ~/.local/share/bash-completion/completions/")
    
    print("\nZsh:")
    print("  # Add to a directory in your $fpath, e.g.:")
    print("  cp completions/_smarttree ~/.zsh/completions/")
    print("  # Then add to ~/.zshrc: fpath=(~/.zsh/completions $fpath)")
    
    print("\nFish:")
    print("  cp completions/smarttree.fish ~/.config/fish/completions/")

if __name__ == "__main__":
    main()