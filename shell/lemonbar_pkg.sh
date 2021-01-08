#!/usr/bin/env sh
# Checks how many packages need updating

#Need to update or it wont know there are new packages

# TODO; test if works with empty list
ignore_list="(^$(rg "^Ignore.*" /etc/pacman.conf | sed -e 's/^.*= //' -e 's/ /$)|(^/g')$)"

while true; do
    sudo pikaur -Sy > /dev/null 2>&1

    pac=$(pacman -Qqu | rg --invert-match --count "$ignore_list")
    [ -z $pac ] && pac=0

    aur=$(pikaur -Qqu 2> /dev/null | rg --invert-match --count "$ignore_list")
    ## Need to minus 1 since pikaur outputs a non-blank blank line
    #aur=$(awk -v a="$aur" 'BEGIN { printf a-1 }')
    aur=$(awk -v a="$aur" -v p="$pac" 'BEGIN { printf a-p }')

    [ "$pac" = "0" ] && [ "$aur" = "0" ] && leader="L" || leader="H"
    echo "P$leader$pac  $aur"

    sleep 3600
done
