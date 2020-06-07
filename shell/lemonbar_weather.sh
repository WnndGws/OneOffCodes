#!/usr/bin/env sh
## Shell script to run get the weather on a loop

while true; do
    WEATHER="$($HOME/git/scripts/python/lemonbar_weather)"
    echo "R""$WEATHER"
    sleep 1800
done
