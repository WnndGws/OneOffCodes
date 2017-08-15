#!/bin/zsh
#Lists the 10 largest folders in specified folder

pat="$1"
shift
if [ "$#" = "0" ]; then
  set "."
fi
find $pat -maxdepth 1 -type d -print0 |
    xargs -0 du --max-depth=1 |
    sort -rn |
    head -n 11 |
    tail -n +2 |
    cut -f2 |
    xargs -I{} du -sh {}
