#!/bin/zsh
## A Simple script to open the correct files with the correct program


# A function containing a case list of options
open() {
    case "$1" in
        *youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi) mpv --x11-name=mpv_youtube --really-quiet --autofit=30% --geometry=-15-55 --ytdl --ytdl-format="mp4[height<=?720]" "$1" &! ;;
        *.png|*.jpeg|*.gif*|*.jpg) feh -. "$1";;  # feh -. = opens to fit window.
        *) google-chrome-stable "$1";  # For everything else.;
    esac
}

# Now a for loop to iterate the list of options,
for url; do
    open "$url"
done
