#!/usr/bin/zsh
## Sets the display brightness to match battery level

battery_percentage=$(acpi --battery | rg -o '[0-9]{2}%')

if [[ -z $battery_percentage ]]; then
    break
else
    xbacklight -set $battery_percentage
fi
