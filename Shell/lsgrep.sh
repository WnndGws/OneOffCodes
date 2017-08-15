#!/bin/zsh
#Allows me to find a file or folder, list them, and open a chosen one. My not elegant solution to a common problem

IFS=$'\n'
# Internal Field Seperator is newlines

if [ "$#" -eq "1" ]; then
    if [[ "$1" =~ "\+" ]];then
        pat=$(echo "$1" | sed 's|+|\.\*|')
    else
        pat="$1"
    fi
    arr=( $(find ~ -iname "*$pat*" 2>/dev/null))
    echo "Choose a file/folder to open: \033[0K\r"
    select opt in ${arr[@]}; do
        xdg-open $opt> /dev/null 2>&1; break
    done
# If only one argument set path to search in as ~
# If there is a plus symbol in the search term replace it with the regex .*
# Present found to user and let choose

else
    if [[ "$2" =~ "\+" ]];then
        pat=$(echo "$2" | sed 's|+|\*|')
    else
        pat="$2"
    fi
    echo "Choose a file/folder to open: \033[0K\r"
    arr=( $(find $1 -iname "*$pat*" 2>/dev/null ))
    select opt in "${arr[@]}"; do
        xdg-open $opt >/dev/null 2>&1; break
    done
fi
# If two terms use 1st term as search term, and second as the path
