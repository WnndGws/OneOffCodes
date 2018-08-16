#!/usr/bin/zsh
## Use aria2c to seed my torrents

for file in $(fd . /home/wynand/wynZFS/Media/ --hidden -e torrent); do
    directory=$(dirname $file)
    aria2c --bt-detach-seed-only --bt-seed-unverified $file --dir $directory & disown
done
