# bash completion for smarttree
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
