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

x=$(echo -e "mpv\nmpv (loop)\numpv\nfeh\nfirefox\nlink_handler\nlink_handler (no summary)" | dmenu -h 40 -fn "Sauce Code Pro Nerd Font Complete Mono:pixelsize=14;0" -i -p "How should I open '$visual'?")
case "$x" in
	mpv) mpv -quiet "$1" 2&>/dev/null & disown ;;
	"mpv (loop)") zsh -c mpv -quiet --loop "$1" 2&>/dev/null & disown ;;
	umpv) $HOME/Git/OneOffCodes/Python/umpv "$1" 2&>/dev/null & disown ;;
	firefox) firefox "$1" 2&>/dev/null & disown ;;
	feh) rm -rf /tmp/images/* ; python $HOME/Git/OneOffCodes/Python/image_scraper/image_scraper.py --url "$1" ; feh --scale-down --recursive /tmp/images & disown;;
	link_handler) urxvtc -hold -e $BROWSER "$1";;
	"link_handler (no summary)") urxvtc -hold -e ~/Git/OneOffCodes/Shell/openWith_NoSummary.sh "$1";;
esac
