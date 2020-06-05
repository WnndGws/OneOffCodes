#!/bin/sh
## Battery display in lemonbar

while true; do
    BAT_PERC=$(($(paste /sys/class/power_supply/BAT0/capacity)))
    BAT_STATE=$(paste /sys/class/power_supply/BAT0/status)
    BAT_CHARGE=$(($(paste /sys/class/power_supply/BAT0/charge_now)))
    BAT_CURR=$(($(paste /sys/class/power_supply/BAT0/current_now)))
    BAT_CAPACITY=$(($(paste /sys/class/power_supply/BAT0/charge_full)))

    #Need to multiply by 100 to get 3 digits, as shell doesnt work with floating points
    TIME_FULL=$(printf "%03d" $(((((BAT_CAPACITY - BAT_CHARGE)*100)/BAT_CURR))))
    #keep only the 1st digit, as the output is given in hours
    TIME_FULL_H=$(printf "%-.1s" "$TIME_FULL")
    #Convert the "decimal" to minutes by stripping the first character, multiplying by 60, then dividing by the original 100
    TIME_FULL_M=$(printf "%-.2s" "$(((${TIME_FULL#?}*6)))")

    TIME_EMPTY=$(printf "%03d" $((((BAT_CHARGE*100)/BAT_CURR))))
    TIME_EMPTY_H=$(printf "%-.1s" "$TIME_EMPTY")
    TIME_EMPTY_M=$(printf "%-.2s" "$(((${TIME_EMPTY#?}*6)))")

    FONT_COLOUR="#eee8d5" # white

    if [ "$BAT_STATE" = "Charging" ] || [ "$BAT_STATE" = "Full" ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" #green
        TIME="$TIME_FULL_H""h:""$TIME_FULL_M""m"
    elif [ "$BAT_PERC" -gt 75 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" #green
        TIME="$TIME_EMPTY_H""h:""$TIME_EMPTY_M""m"
    elif [ "$BAT_PERC" -gt 50 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" #yellow
        TIME="$TIME_EMPTY_H""h:""$TIME_EMPTY_M""m"
    elif [ "$BAT_PERC" -gt 15 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" #yellow
        TIME="$TIME_EMPTY_H""h:""$TIME_EMPTY_M""m"
    else
        ICON=""
        UNDERLINE_COLOUR="#e65350" #red
        TIME="$TIME_EMPTY_H""h:""$TIME_EMPTY_M""m"
    fi

    printf "%s\n" "B[%{F$FONT_COLOUR}%{U$UNDERLINE_COLOUR} %{+u}${ICON} ${BAT_PERC}% (${TIME})%{-u} %{U-}%{F-}]"
    sleep 120
done
