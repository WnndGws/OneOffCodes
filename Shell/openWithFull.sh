#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif) mpv --really-quiet --ytdl --ytdl-format="mp4[height<=?720]" "$1" &! ;;
        *.png|*.jpeg|*.jpg) feh -. --geometry 600x600 "$1";;  # feh -. = opens to fit window.
        *) google-chrome-stable "$1";  # For everything else.;
    esac
}

# Now a for loop to iterate the list of options,
for url; do
    open "$url"
done
