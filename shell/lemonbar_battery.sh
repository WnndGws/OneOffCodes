#!/bin/sh
## Battery display in lemonbar

while true; do
    BAT_PERC=$(($(paste /sys/class/power_supply/BAT0/capacity)))
    BAT_STATE=$(paste /sys/class/power_supply/BAT0/status)

    FONT_COLOUR="#eee8d5" # white

    if [ "$BAT_STATE" = "Charging" ] || [ "$BAT_STATE" = "Full" ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" #green
    elif [ "$BAT_PERC" -gt 75 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" #green
    elif [ "$BAT_PERC" -gt 50 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" #yellow
    elif [ "$BAT_PERC" -gt 25 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" #yellow
    else
        ICON=""
        UNDERLINE_COLOUR="e65350" #red
    fi

    printf "%s\n" "B[%{F$FONT_COLOUR}%{U$UNDERLINE_COLOUR} %{+u}${ICON} ${BAT_PERC}%%{-u} %{U-}%{F-}]"
    sleep 300
done