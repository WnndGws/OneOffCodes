#!/bin/zsh
#Allows user to enter shutdown_in hh:mm:ss and gives a countdown, had to change shutdown command to not need sudo, thus no need to expect in pw, although could do it that way

timein=$1
delimiter=":"
numberOfDelimiters=$(grep -o "$delimiter" <<< $timein | wc -l)
## Tests the format that time_in is given by counting how many ":" there are

if [[ $numberOfDelimiters == "1" ]]; then
    ((time_ts=$(echo "$1" | awk -F: '{ print ($1*60) + $2 }')))
elif [[ $numberOfDelimiters == "2" ]]; then
    ((time_ts=$(echo "$1" | awk -F: '{ print ($1*60*60) + ($2*60) + $3 }')))
elif [[ $numberOfDelimiters == "3" ]]; then
    ((time_ts=$(echo "$1" | awk -F: '{ print ($1*24*60*60) + ($2*60*60) + ($3*60) + $4 }')))
else
    break
fi
## If number of delims is 1 then assume argument is seconds, 3 is hh:mm:ss

while [ $time_ts -gt 0 ]; do
    echo -ne "Shutdown will occur in $time_ts seconds......\033[0K\r"
    sleep 1
    ((time_ts--))
done
## Countdown in terminal

sudo shutdown
## Had to set linux to run shutdown without confirmation
