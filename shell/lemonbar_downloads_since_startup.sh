#!/usr/bin/env sh
## Checks the downloads since I use 4g hotspot

start_rx=$(paste /sys/class/net/wlan0/statistics/rx_bytes)

while true; do
    now_rx=$(paste /sys/class/net/wlan0/statistics/rx_bytes)
    total_rx=$(awk -v s="$start_rx" -v n="$now_rx" 'BEGIN { printf n-s }')
    humanized_rx=$(units "$total_rx bytes" megabytes | awk 'NR==1 { printf "%d", $2 }')
    printf "%s" D"$humanized_rx"Mb
    sleep 30
done
