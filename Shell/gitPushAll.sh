#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"$HOME/Git/OneOffCodes"
"$HOME/Git/OneOffCodes/Expects"
"$HOME/Git/OneOffCodes/Python"
"$HOME/Git/OneOffCodes/Shell"
"$HOME/Git/DS18B20_email_alert"
)

for i in "${repos[@]}"; do
    cd "$i"

    for file in $(git ls-files --others --exclude-standard); do
        git add $file
        git commit -vS
    done

    for file in $(git diff --name-only)
        git add -p $file
        git commit -vS
    done

git push
