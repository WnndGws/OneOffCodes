#!/usr/bin/zsh
## Sets the display brightness to match battery level

battery_percentage=$(acpi --battery | rg -o '[0-9]{2}%')
battery_state=$(acpi --battery | awk '{print $3}')

if [[ $battery_state == "Charging," ]]; then
    brightnessctl --device=acpi_video0 s 100%
else
    if [[  $battery_percentage != "00%" ]]; then
        brightnessctl --device=acpi_video0 s $battery_percentage
    fi
fi
