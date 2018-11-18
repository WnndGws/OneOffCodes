#!/usr/bin/zsh
## Sleep until a certain time

timein=$1
delimiter=":"
nowtime=$(date -d now +%s)
shutdowntime=$(date -d $1 +%s)

## If sleep_until is tomorrow, then add the amount of seconds
if [ $shutdowntime -le $nowtime ]; then
    shutdowntime=$(date -d $1 +%T)
    shutdowntime=$(echo "$(date -d $shutdowntime +%s) + 86400" | bc)
fi

time_ts=$(echo "$shutdowntime - $nowtime" | bc)

while [ $time_ts -gt 0 ]; do
    echo -ne "Sleep will end in $(date -u -d @$time_ts +'%T')......\033[0K\r"
    sleep 1
    ((time_ts--))
done
# Countdown in terminal
