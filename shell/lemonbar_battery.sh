#!/usr/bin/env zsh
## Battery display in lemonbar
## Note: this uses bashisms so not strictly POSIX

FONT_COLOUR="#eee8d5" # white

print_state() {
    BAT_PERC=$(($(paste /sys/class/power_supply/BAT0/capacity)))
    BAT_STATE=$(paste /sys/class/power_supply/BAT0/status)

    if [ $BAT_STATE = "Full" ]; then
        TIME=$BAT_STATE
    else
        TIME=$(acpi)
        TIME=${TIME%:*}
        TIME=${TIME##* }
    fi

    if [ "$BAT_STATE" = "Charging" ]; then
        ICON="" # fontawesome 'plug' (f1e6)
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 95 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 75 ]; then
        ICON=""
        UNDERLINE_COLOUR="#99c76c" # green
    elif [ "$BAT_PERC" -gt 50 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" # yellow
    elif [ "$BAT_PERC" -gt 15 ]; then
        ICON=""
        UNDERLINE_COLOUR="#ffc24b" # yellow
    else
        ICON=""
        UNDERLINE_COLOUR="#e65350" # red
    fi

    printf "%s\n" "B[%{F$FONT_COLOUR}%{U$UNDERLINE_COLOUR} %{+u}${ICON} ${BAT_PERC}% (${TIME})%{-u} %{U-}%{F-}]"
}

check_state_change() {
    unset changed
    BAT_STATE_OLD=$(paste /sys/class/power_supply/BAT0/status)
    sleep 1
    BAT_STATE_NEW=$(paste /sys/class/power_supply/BAT0/status)

    if [[ "$BAT_STATE_OLD" != "$BAT_STATE_NEW" ]]; then
        changed=true
    fi
}

# Need to do initial print when script runs, otherwise it will wait until divisible by 5
print_state
while true; do
    check_state_change
    if [[ $changed == true ]]; then
        print_state
    fi
    SYS_TIME=$(date +"%M")
    if [[ $((SYS_TIME % 5)) == "1" ]]; then
        unset recently_changed
    fi
    # Check if remainder of Current time's mins is 0, then
    if [[ $((SYS_TIME % 5)) == "0" ]] && [[ $recently_changed != 1 ]]; then
        print_state
        recently_changed=1
    fi
done
