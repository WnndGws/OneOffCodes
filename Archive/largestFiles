#!/bin/zsh
##Lists the 10 largest files in the given dir

pat="$1"
shift
if [ "$#" = "0" ]; then
  set "."
fi
find $pat -type f -print0 |
    xargs -0 du |
    sort -rn |
    head -n 10 |
    cut -f2 |
    xargs -I{} du -sh {}
