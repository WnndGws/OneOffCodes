#!/usr/bin/env sh
## reads volume

## TODO check if muted, write a vol-change script
getCurVol() { volume=$(($(pamixer --get-volume)))
        if [ $volume -gt 50 ]; then
            leader="VH"
            icon=""
        elif [ $volume -gt 25 ]; then
            leader="VM"
            icon=""
        else
            leader="VL"
            icon=""
        fi
}

#Need to print something, otherwise it waits for 1st event
getCurVol
printf "%s\n" "${leader}${icon}${volume}"

#Subscribe, and for each line print the current volume
pactl subscribe | grep --line-buffered "sink" |\
    while read -r line; do
        getCurVol
        printf "%s\n" "${leader}${icon}${volume}"
    done
