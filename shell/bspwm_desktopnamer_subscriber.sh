#!/usr/bin/env sh
## Subscribes to bspc and runs script when needed

bspc subscribe node_add node_remove node_transfer node_focus | while read -r _; do
    /home/wynand/git/scripts/shell/bspwm_desktopnamer.sh
done
