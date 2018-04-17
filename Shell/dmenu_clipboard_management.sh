#!/bin/zsh
# Feed this script a link and it will give dmenu
# some choice programs to use to open it.

x=$(echo -e "clip->primary\nprimary->clip\npaste" | dmenu -h 40 -fn "Sauce Code Pro Nerd Font Complete Mono:pixelsize=12;0" -i -p "Where should I copy to/from?")
case "$x" in
	"clip->primary") xsel -ob | xsel -ip ;;
	"primary->clip") xsel -op | xsel -ib ;;
	"paste") xsel -ob | xsel -ip && xsel -op 2> /dev/null ;;
esac
