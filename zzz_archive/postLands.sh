#!/bin/zsh
## Puts computer back to it's "normal" state

redshift -l 31.57:115.51 -b 1:0.65 -t 5500:2000 &!
#nmcli con up id USA\ -\ Los\ Angeles
amixer sset 'Master' 50%
rm -f $HOME/nohup.out
killall -9 steam
killall -9 obs
