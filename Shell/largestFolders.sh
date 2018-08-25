#!/bin/zsh
#Lists the 10 largest folders in specified folder

pat="./$1"
shift
if [ "$#" = "0" ]; then
  set "."
fi
find $pat -maxdepth 1 -type d -print0 |
    xargs -I{} -0 du --max-depth=0 "{}" |
    sort -rn |
    head -n 11 |
    tail -n +2 |
    cut -f2 |
    sed "s/'/\\\'/" |
    xargs -I{} ncdu --color dark -rr -x -f - {}
