#!/usr/bin/env sh
## Runs ./bspwm_get_desktops and appends them to the sxhkdrc

# Delete the last 3 lines of the file
sed -i '$d' "$XDG_CONFIG_HOME/sxhkd/sxhkdrc" | sed '$d' | sed '$d'

# Append output of script to the file
$HOME/git/scripts/shell/bspwm_output_desktops.sh >> "$XDG_CONFIG_HOME/sxhkd/sxhkdrc"
