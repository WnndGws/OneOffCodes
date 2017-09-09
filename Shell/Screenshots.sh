#!/bin/zsh

echo "Select area to share......"
sleep 0.1
scrot '/home/wynand/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots/%Y-%m-%d-%T.png' -q 100 -a
file_to_share=$(find /home/wynand/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" " | sed 's/\.\//\/home\/wynand\/GoogleDrive\/01_Personal\/01_Personal\/05_Images\/Screenshots\//g')
xclip -selection clipboard -t image/png -i $file_to_share
secs=$((15))
while [ $secs -gt 0 ]; do
   echo -ne "Paste image within the next $secs seconds....\033[0K\r"
   sleep 1
   : $((secs--))
done
find /home/wynand/GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots -type f -mtime +7 -execdir rm -f {} \;
