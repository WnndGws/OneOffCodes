#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
#"$HOME/Git/DS18B20_email_alert"
"$HOME/Git/OneOffCodes"
"$HOME/Git/OneOffCodes/Expects"
"$HOME/Git/OneOffCodes/Python"
"$HOME/Git/OneOffCodes/Shell"
"$HOME/Git/WnndGws.github.io"
)

if [[ $(ssh-add -l) == 0 ]]; then
    ssh-add
fi

for i in "${repos[@]}"; do
    cd "$i"
    git pull

    for file in $(git ls-files --others --exclude-standard); do
        git add $file
        git commit -vS $file
    done

    for file in $(git diff --name-only); do
        git add -p $file
        git commit -vS $file
    done

    git push
done

