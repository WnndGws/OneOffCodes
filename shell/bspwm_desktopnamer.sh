#!/usr/bin/env sh
## Script to use bspc subscribe to constantly watch windows

bspc subscribe node_{add,remove} | while read -r line; do
    $HOME/Git/scripts/python/bspwm_desktopnamer
done
