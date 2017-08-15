#!/bin/zsh
## Get my pc ready to play online games

nmcli con down id USA\ -\ Los\ Angeles
redshift -x
kill $(pgrep redshift)
nohup obs &
amixer sset 'Master' 85%
nohup steam-native &
