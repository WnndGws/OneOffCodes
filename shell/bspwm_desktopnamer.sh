#!/usr/bin/env sh
## Script to use bspc subscribe to constantly watch windows

bspc subscribe node_{add,remove,transfer} | while read -r line; do
    "$HOME/git/scripts/python/bspwm_desktopnamer"
done
