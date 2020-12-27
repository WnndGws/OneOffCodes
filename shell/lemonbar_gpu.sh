#!/bin/sh
# Checks how many packages need updating

#Need to update or it wont know there are new packages
while true; do
    # Get 10th row, 3rd collumn and strip last character
    temp=$(nvidia-smi | awk 'NR==10 {print substr($3, 1, length($3)-1)}')
    usage=$(nvidia-smi | awk 'NR==10 {print substr($13, 1, length($13))}')

    echo "G $usage ($temp°C)"

    sleep 2
done
