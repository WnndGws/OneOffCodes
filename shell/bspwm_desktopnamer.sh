#!/usr/bin/env sh
## Renames my desktops depending whats open on them

# Define icons
icon_list="
Alacritty 
MozillaFirefox 
NVim 
MPV 
JFTUI ﴽ
Newsboat 
Zathura 
Neomutt 﫮
SignalBeta 
Pidgin 
Feh 﨤
Steam 
"

#bspc subscribe node_add node_remove desktop_transfer | while read -r _; do
# Get all desktops
desktops=$(bspc query --desktops)

# Get list of all windows on all desktops
window_list=$(wmctrl -l -x)

# Set desktop number itterator
desktop_number=0

for desktop in $desktops; do
    # Start counting desktops
    desktop_number=$((desktop_number + 1))
    window_string="$desktop_number"
    winids_on_desktop=$(bspc query --nodes --node .window --desktop "$desktop")

    for window_id in $winids_on_desktop; do
        window=$(printf "%s" "$window_list" | grep -i "$window_id")
        window_class=$(printf "%s" "$window" | cut -d'.' -f2 | cut -d' ' -f1)
        if [ "$window_class" = "alacritty" ]; then
            window_name=$(printf "%s" "$window" | rev | cut -d"-" -f1 | rev | sed 's/\ //g' | sed 's/ARCH//g')
            window_icon=$(printf "%s" "$icon_list" | grep -i "$window_name" | cut -d' ' -f2)
        else
            window_icon=$(printf "%s" "$icon_list" | grep -i "$window_class" | cut -d' ' -f2)
        fi
        [ -z "$window_icon" ] && window_icon="x"
        window_string="$window_string"" $window_icon"
    done
    bspc desktop "$desktop" --rename "$window_string"
done
