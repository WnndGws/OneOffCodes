#!/usr/bin/zsh
## Use aria2c to seed my torrents

file="$1"
file_name=$(echo $file | rev | cut -d'/' -f1 | cut -d'.' -f2- | rev | cut -d'.' -f2-)
directory=$(dirname $file)
aria2c --bt-force-encryption --bt-require-crypto --bt-max-peers=0 --bt-detach-seed-only --bt-seed-unverified $file --dir $directory --index-out=1=$file_name.mkv