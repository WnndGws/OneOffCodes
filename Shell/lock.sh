#!/bin/zsh
## Locks and mutes PC

amixer sset 'Master' 00%
# Mutes

scrot /tmp/screen.png
convert /tmp/screen.png -scale 10% -scale 100% /temp/screen.png
[[ -f ~/.dotfiles/i3/.config/i3/lock.png ]] && convert /tmp/screen.png ~/.dotfiles/i3/.config/i3/lock.png -gravity center -composite -matte /tmp/screen.png


i3lock --no-unlock-indicator --ignore-empty-password --image=/tmp/screen.png
trash-empty
xset dpms force off
# Turns off screen
