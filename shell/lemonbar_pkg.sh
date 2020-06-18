#!/bin/sh
# Checks how many packages need updating

#Need to update or it wont know there are new packages
while true; do
    pikaur -Sy > /dev/null 2>&1

    pac=$(pacman -Qqu 2> /dev/null | wc -l)
    aur=$(pikaur -Qqu 2> /dev/null | wc -l)
    aur=$(awk -v a='$aur' -v p='$pac' 'BEGIN { printf a-b }')

    [ "$pac" = " 0" ] && [ "$aur" = "0" ] && leader="L" || leader="H"
    echo "P$leader$pac  $aur"

    sleep 3600
done
