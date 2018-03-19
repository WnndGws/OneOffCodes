#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *stream*|*gfycat*|*v.redd.it*|*imgtc*|*youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif|*vimeo|*vimeo.com*) $HOME/Git/OneOffCodes/Python/umpv "$1" &! ;;
        *imgur*|*.png*|*.jpeg*|*.jpg*) feh --scale-down "$1";;  # feh -. = opens to fit window.
        *) others "$1"
        #*) firefox "$1";  # For everything else.;
    esac
}

others(){
rm -f /tmp/image*
rm -f /tmp/para.txt 
python $HOME/Git/OneOffCodes/Python/paragraph_scraper/paragraph_scraper.py --url "$1" > /dev/null 2>&1
if [[  $(wc -l /tmp/para.txt | awk '{print $1}') > 0  ]]
then
    urxvtc -geometry 50x2 -e speedread -w 375 /tmp/para.txt
    python $HOME/Git/OneOffCodes/Python/image_scraper/image_scraper.py --url "$1" > /dev/null 2>&1
    find /tmp/image* -print0 | xargs -0 identify -format "%w %f\n" | awk '$1<200' | xargs -0 | cut -d' ' -f2 | xargs -I{} rm /tmp/{}
    feh --scale-down /tmp/image*
else
    firefox "$1"
fi
}

# Now a for loop to iterate the list of options,
for url; do
    echo "$url" | xclip -selection clipboard
    open "$url"
done
