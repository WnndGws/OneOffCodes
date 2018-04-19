#!/usr/bin/zsh
# A dmenu binary prompt script.
# Gives a dmenu prompt labeled with $1 to perform command $2.
# For example:
# `./prompt "Do you want to shutdown?" "shutdown -h now"`

[[ $(echo -e "No\nYes" | dmenu -i -p "$1" -h 40 -fn "Sauce Code Pro Nerd Font Complete Mono:pixelsize=14;0") \
== "Yes" ]] && zsh -c $2 

