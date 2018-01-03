#!/usr/bin/zsh
## Sets the display brightness to match battery level

battery_percentage=$(acpi --battery | rg -o '[0-9]{2}%')

if [[  $battery_percentage == "00%" ]]; then
    break
else
    brightnessctl s $battery_percentage
fi
