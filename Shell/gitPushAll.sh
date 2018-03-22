#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"$HOME/Git/OneOffCodes"
"$HOME/Git/OneOffCodes/Expects"
"$HOME/Git/OneOffCodes/Python"
"$HOME/Git/OneOffCodes/Shell"
)

for i in "${repos[@]}"; do
    cd "$i"
    while [[ $(git status . | tail -n 1) != "nothing to commit, working tree clean" ]]; do

        for file in $(git ls-files --others --exclude-standard); do
            git add $file
            git commit -oS $file
        done

        for file in $(git diff --name-only); do
            git add -p $file
            git commit -oS $file
        done
    done

    git push
done
