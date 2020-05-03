#!/bin/zsh
## Pings google.com, and if fails it resets network interface

connected_network=$(iwgetid | grep -o "\".*\"" | sed 's/\"//g')
echo $connected_network
sleep_time=1
time_elapsed=0
timeout 1.0 ping -c1 google.com
exit_code=$(echo $?)
echo $exit_code

while /bin/true; do
    timeout 1.0 ping -c1 google.com
    exit_code=$(echo $?)
    if [[ "$exit_code" -eq 124 ]]; then
        sleep 3
        timeout 1.0 ping -c1 google.com
        exit_code=$(echo $?)
        if [[ "$exit_code" -eq 124 ]]; then
            notify-send "Resetting Network" "Reset occurring $(date -u -d @$time_elapsed +'%T') after last reset" --icon=network-wireless -t 10000 -u low
            nmcli con up id $connected_network
            sleep_time=1
            time_elapsed=0
            sleep 10
        fi
    elif [[ "$sleep_time" -gt 600 ]]; then
        echo "Sleeping for 600"
        sleep 600
    else
        time_elapsed=$(echo "$time_elapsed + $sleep_time" | bc)
        sleep_time=$(echo "$sleep_time * 1.5" | bc)
        echo "Sleeping for $sleep_time"
        sleep $sleep_time
    fi
done
