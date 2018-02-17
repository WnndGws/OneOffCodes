#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"$HOME/Git/CarPi-Diem"
"$HOME/Git/OneOffCodes"
"$HOME/Git/OneOffCodes/Expects"
"$HOME/Git/OneOffCodes/Python"
"$HOME/Git/OneOffCodes/Shell"
)

for i in "${repos[@]}"; do
    cd "$i"
    for file in $(git ls-files --others --exclude-standard); do
        git add $file
        git commit -oS $file
        git tag -a
    done

    for file in $(git diff --name-only); do
        git add -p $file
        git commit -oS $file
        git tag -a
    done

    git push
done
