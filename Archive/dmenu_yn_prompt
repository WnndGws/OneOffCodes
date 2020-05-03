#!/usr/bin/zsh
# A dmenu binary prompt script.
# Gives a dmenu prompt labeled with $1 to perform command $2.
# For example:
# `./prompt "Do you want to shutdown?" "shutdown -h now"`

[[ $(echo -e "Yes\nNo" | dmenu -i -p "$1" -h 40 -fn "CodeNewRoman Nerd Font:pixelsize=15;1") \
== "Yes" ]] && zsh -c $2 

