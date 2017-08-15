#!/bin/zsh
## Locks and mutes PC

amixer sset 'Master' 00%
# Mutes

i3lock -c 000000
trash-empty
xset dpms force off
# Turns off screen
