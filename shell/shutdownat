#!/bin/zsh
#Allows user to enter shutdown time in human readable format and gives a countdown, had to change shutdown command to not need sudo, thus no need to expect in pw, although could do it that way

timein=$1
delimiter=":"
shutdowntime=$(date -d $1 +%T)
shutdowntime=$(echo "$(date -d $shutdowntime +%s) + 86400" | bc)
nowtime=$(date -d now +%s)
time_ts=$(echo "$shutdowntime - $nowtime" | bc)

while [ $time_ts -gt 0 ]; do
    echo -ne "Shutdown will occur in $(date -u -d @$time_ts +'%T')......\033[0K\r"
    sleep 1
    ((time_ts--))
done
# Countdown in terminal

systemctl poweroff
