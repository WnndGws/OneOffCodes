#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"~/Git/CarPi-Diem"
"~/Git/OneOffCodes"
"~/Git/OneOffCodes/Expects"
"~/Git/OneOffCodes/Python"
"~/Git/OneOffCodes/Shell"
)

for i in "${repos[@]}"; do
    cd "$i"
    for file in $(git ls-files --others --exclude-standard); do
        git add $file
        git commit -oS $file
    done

    for file in $(git diff --name-only); do
        git add -p $file
        git commit -oS $file
    done

    git push
done
