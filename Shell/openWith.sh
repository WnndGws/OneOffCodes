#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *streamable*|*gfycat*|*v.redd.it*|*imgtc*|*youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif) $HOME/Git/OneOffCodes/Python/umpv "$1" &! ;;
        *imgur*|*.png*|*.jpeg*|*.jpg*) feh --scale-down "$1";;  # feh -. = opens to fit window.
        *) rm -f /tmp/image* ; rm -f /tmp/para.txt ; python $HOME/Git/OneOffCodes/Python/paragraph_scraper.py --url "$1" > /dev/null 2>&1 ; feh --scale-down /tmp/image* & urxvtc -geometry 50x2 -e speedread -w 375 /tmp/para.txt
        #*) google-chrome-stable "$1";  # For everything else.;
    esac
}

# Now a for loop to iterate the list of options,
for url; do
    echo "$url" | xclip -selection clipboard
    open "$url"
done
