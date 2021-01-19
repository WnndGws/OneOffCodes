#!/usr/bin/env zsh
# Checks GPU stats

# Need to update or it wont know there are new packages
while true; do
    # Get 4th row, 2nd column and strip last character
    temp=$(sensors | rg --after-context 3 "amdgpu" | awk 'NR==4 {print substr($2, 2, length($2)-5)}')
    usage=$(radeontop --dump - | rg --only-matching --pcre2 --max-count 1 "(?<=gpu )\d\.\d{2}")
    usage=$(printf "%2d" $usage)

    echo "G $usage% ($temp°C)"

    sleep 2
done
