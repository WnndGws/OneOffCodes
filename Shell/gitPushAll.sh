#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"/home/wynand/Git"
"/home/wynand/Git/OneOffCodes"
"/home/wynand/Git/OneOffCodes/Expects"
"/home/wynand/Git/OneOffCodes/Python"
"/home/wynand/Git/OneOffCodes/Shell"
)

for i in "${repos[@]}"; do
    cd "$i"
    git add .
    git commit -aS
    git pull
    git push
done
