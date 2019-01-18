#!/usr/bin/zsh
## Use aria2c to seed my torrents

file="$1"
aria2c --show-files $file
echo -n "Index number of desired torrent: "
read file_number
file_name=$(echo $file | rev | cut -d'/' -f1 | cut -d'.' -f2- | rev | cut -d'.' -f2-)
directory=$(dirname $file)
aria2c --max-overall-download-limit=1M --bt-force-encryption=true --bt-require-crypto=true --bt-max-peers=0 --bt-detach-seed-only=true --bt-seed-unverified=true $file --dir $directory --select-file="$file_number" --index-out="$file_number"=$file_name.mkv
