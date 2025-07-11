# Fish completion for smarttree
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
