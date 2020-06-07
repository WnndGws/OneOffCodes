#!/bin/sh
#Checks how much is being downloaded to calc a speed

while true; do
    ## All these brackets interprets output as a number
    down_past=$(($(paste /sys/class/net/wlan0/statistics/rx_bytes)))
    up_past=$(($(paste /sys/class/net/wlan0/statistics/tx_bytes)))
    sleep 1
    down_now=$(($(paste /sys/class/net/wlan0/statistics/rx_bytes)))
    up_now=$(($(paste /sys/class/net/wlan0/statistics/tx_bytes)))

    #Prints out the digit padded to length 4
    #Divides by 2000 since 2000 bytes in a kilobyte, and divides by 2 since the sum includes lo and wlp0s29u1u5, where lo is this session, and wlp is a running total, so each byte is counted twice
    down_per_sec=$(printf " %4d kB/s" $(((down_now - down_past)/1024)))
    up_per_sec=$(printf " %4d kB/s" $(((up_now - up_past)/1024)))

    #echo "W$down_per_sec | $up_per_sec"
    echo "W$down_per_sec"
done
