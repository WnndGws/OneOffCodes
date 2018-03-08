#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *streamable*|*gfycat*|*v.redd.it*|*imgtc*|*youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif) mpv "$1" &! ;;
        *imgur*|*.png*|*.jpeg*|*.jpg*) feh --scale-down "$1";;  # feh -. = opens to fit window.
        *) google-chrome-stable "$1";  # For everything else.;
    esac
}

# Now a for loop to iterate the list of options,
for url; do
    echo "$url" | xclip -selection clipboard
    open "$url"
done
