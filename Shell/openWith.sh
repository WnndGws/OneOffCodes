#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *gfycat*|*v.redd.it*|*imgtc*|*youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif) mpv --really-quiet --loop "$1" &! ;;
        *.png*|*.jpeg*|*.jpg*) feh --scale-down "$1";;  # feh -. = opens to fit window.
        *) w3m -dump "$1" > /tmp/tmp.txt && urxvt -e vim /tmp/tmp.txt && rm /tmp/tmp.txt
        #*) google-chrome-stable "$1";  # For everything else.;
    esac
}

# Now a for loop to iterate the list of options,
for url; do
    open "$url"
done
