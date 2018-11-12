#!/usr/bin/zsh
## Sleep until a certain time

timein=$1
delimiter=":"
shutdowntime=$(date -d $1 +%T)
shutdowntime=$(echo "$(date -d $shutdowntime +%s) + 86400" | bc)
nowtime=$(date -d now +%s)
time_ts=$(echo "$shutdowntime - $nowtime" | bc)

while [ $time_ts -gt 1 ]; do
    echo -ne "Sleep will end in $(date -u -d @$time_ts +'%T')......\033[0K\r"
    sleep 1
    ((time_ts--))
done
# Countdown in terminal
