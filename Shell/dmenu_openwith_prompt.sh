#!/bin/zsh
# Feed this script a link and it will give dmenu
# some choice programs to use to open it.

# The URL will be shown visually in 30 characters or less.
if [[ "${#1}" -gt 30 ]];
then
visual="${1:0:20}"..."${1: -7}"
else
visual="$1"
fi
echo $visual

x=$(echo -e "umpv_180p\numpv\nmpv\nmpv_loop\nfeh\nfirefox\nparagraph\nsummary\nytdl" | dmenu -h 40 -fn "CodeNewRoman Nerd Font:pixelsize=15;1" -i -p "How should I open '$visual'?")
case "$x" in
    summary) clear; rm -f /tmp/para* > /dev/null 2>&1; python $HOME/Git/OneOffCodes/Python/paragraph_scraper/paragraph_scraper.py --url "$1"; python $HOME/Git/OneOffCodes/Python/paragraph_scraper/article_summarise.py; gvim /tmp/para_summarise.txt;;
	umpv) clear; python $HOME/Git/OneOffCodes/Python/umpv "$1" > /dev/null 2>&1 & disown ;;
	umpv_180p) clear; python $HOME/Git/OneOffCodes/Python/umpv_180p "$1" > /dev/null 2>&1 & disown ;;
	mpv) clear; mpv --ytdl-format="best[height<=720]" --quiet "$1" 2&>/dev/null & disown ;;
	mpv_loop) clear; mpv -quiet --loop "$1" 2&>/dev/null & disown ;;
	firefox) clear; firefox "$1" 2&>/dev/null & disown ;;
	feh) clear; rm -rf /tmp/images/* 2>&1 /dev/null; gallery-dl --dest /tmp/images "$1" >/dev/null 2>&1 ; feh --scale-down --recursive /tmp/images --title "%S %n" & disown;;
    paragraph) clear; rm -f /tmp/para* > /dev/null 2>&1; python $HOME/Git/OneOffCodes/Python/paragraph_scraper/paragraph_scraper.py --url "$1"; gvim /tmp/para.txt ;;
    ytdl) clear; youtube-dl "$1" > /dev/null 2>&1 & ;;
    *) "$x" "$1"
esac
