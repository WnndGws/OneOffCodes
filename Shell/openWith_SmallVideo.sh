#!/bin/zsh
## A Simple script to open the correct files with the correct program
## Same as openwith, but doesnt set mpvf lag to make it seethrough and float

# A function containing a case list of options
open() {
    case "$1" in
        *stream*|*gfycat*|*v.redd.it*|*imgtc*|*youtube.com*|*youtu.be*|*vodlocker.com*|*.webm*|*.mp4*|*.avi|*.gif|*vimeo|*vimeo.com*) $HOME/Git/OneOffCodes/Python/umpv_180p "$1" &! ;;
        *imgur*|*.png|*.jpeg|*.jpg) rm -rf /tmp/images/* ; gallery-dl --dest /tmp/images "$1" ; feh --scale-down --recursive /tmp/images;;  # feh -. = opens to fit window.
        *) others "$1"
        #*) firefox "$1";  # For everything else.;
    esac
}

others(){
clear
rm -rf /tmp/images/* > /dev/null 2>&1
rm -f /tmp/para.txt > /dev/null 2>&1
rm -f /tmp/para_summarise.txt > /dev/null 2>&1
python $HOME/Git/OneOffCodes/Python/paragraph_scraper/paragraph_scraper.py --url "$1" > /dev/null 2>&1
python $HOME/Git/OneOffCodes/Python/paragraph_scraper/article_summarise.py
if [[  $(wc -l /tmp/para.txt | awk '{print $1}') > 10  ]]
then
    cat /tmp/para_summarise.txt | wc -l
    cat /tmp/para_summarise.txt
    #speedread -w 325 /tmp/para_summarise.txt
    mkdir /tmp/images > /dev/null 2>&1
    gallery-dl --dest /tmp/imgur "$1" > /dev/null 2>&1
    python $HOME/Git/OneOffCodes/Python/image_scraper/image_scraper.py --url "$1" > /dev/null 2>&1
    feh --scale-down --recursive /tmp/images &
    youtube-dl -o "/tmp/images/video.%(ext)s" "$1" > /dev/null 2>&1
    if [ -f /tmp/images/video* ]; then
        mpv /tmp/images/video* > /dev/null 2>&1
    fi
    sleep 14400
else
    firefox "$1"
fi
}

# Now a for loop to iterate the list of options,
for url; do
    echo "$url" | xclip -selection clipboard
    open "$url"
done
