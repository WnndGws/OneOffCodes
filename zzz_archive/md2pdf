#!/usr/bin/zsh
## Uses pandoc to convert a md file to a pdf

file="$1"
file_name=$(echo "$file" | cut -d"." -f1)

pandoc "$file" -t beamer -o "$file_name".pdf
