#!/bin/zsh
## Get my pc ready to play online games

nmcli con down id USA\ -\ Los\ Angeles
redshift -x
kill $(pgrep redshift)
nohup obs --startreplaybuffer &
tilix --maximize --geometry=1440x900+3840+180 -e 'zsh -c "tilix -a session-add-down -e radeontop; tilix -a session-add-right -e sudo nethogs; htop"'
amixer sset 'Master' 85%
nohup steam-native &
