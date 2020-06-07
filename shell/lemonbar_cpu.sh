#!/bin/sh
# Just prints cpu I have available to use in polybar

red='#65350'
green='#99c76c'
yellow='#ffc24b'

while true; do
    # Take one_min core load, times by 100 to get percentage, divide by 4 since quadcore cpu
    one_min_cpu_load_avg=$(awk '{ printf "%1d",$1*25 }' < /proc/loadavg)

    # Start to worry at 70%, investigate at over 100% constantly
    if [ "$one_min_cpu_load_avg" -gt 90 ]; then
        leader="U"
    elif [ "$one_min_cpu_load_avg" -gt 70 ]; then
        leader="H"
    else
        leader="L"
    fi

    echo "C$leader $one_min_cpu_load_avg%"
    sleep 1
done
