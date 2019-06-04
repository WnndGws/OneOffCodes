#!/usr/bin/zsh
## Sets the display brightness to match battery level

battery_percentage=$(acpi --battery | rg -o '[0-9]+%' | awk -F '%' '{print $1}')
set_percentage=$(bc <<< $battery_percentage/1.5)
battery_state=$(acpi --battery | awk '{print $3}')

if [[ $battery_state == "Charging," ]]; then
    brightnessctl --device=acpi_video0 s 100%
else
    if [[  $battery_percentage == "100" ]]; then
        brightnessctl --device=acpi_video0 s 100%
    else
        brightnessctl --device=acpi_video0 s $set_percentage%
    fi
fi
