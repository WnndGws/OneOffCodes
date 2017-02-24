#!/bin/zsh

echo "Select area to share......"
sleep 1
scrot '/home/wynand/GoogleDrive/01_Personal/01_Personal/06_Images/Screenshots/%Y-%m-%d-%T.png' -s
sleep 3
while [[ $(insync get_status) =~ "SYNCING" ]] { sleep 0.5 }
sleep 1
find /home/wynand/GoogleDrive/01_Personal/01_Personal/06_Images/Screenshots -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" " | sed 's/\.\//\/home\/wynand\/GoogleDrive\/01_Personal\/01_Personal\/06_Images\/Screenshots\//g' | xargs -i insync get_link {}
