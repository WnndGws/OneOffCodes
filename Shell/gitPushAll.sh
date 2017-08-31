#!/bin/zsh
## Script to push all my git repos at the same time

declare -a repos=(\
"/home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git"
"/home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes"
"/home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Expects"
"/home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Python"
"/home/wynand/GoogleDrive/01_Personal/01_Personal/01_Git/OneOffCodes/Shell"
)

for i in "${repos[@]}"; do
    cd "$i"
    git add .
    git commit -aS
    git pull
    git push
done
