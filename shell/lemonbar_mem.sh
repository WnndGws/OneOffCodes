#!/usr/bin/env sh
# Just prints memory I have available to use in polybar

while true; do
    free_mem=$(free | awk 'NR==2{ print $7 }')
    tot_mem=$(free | awk 'NR==2{ print $2 }')
    free_percentage=$(awk -v f="$free_mem" -v t="$tot_mem" 'BEGIN { printf "%1d",100*(1-(f/t)) }')

    if [ "$free_percentage" -gt 90 ]; then
        leader="U"
    elif [ "$free_percentage" -gt 75 ]; then
        leader="H"
    elif [ "$free_percentage" -gt 50 ]; then
        leader="M"
    else
        leader="L"
    fi

    echo "M$leader $free_percentage%"
    sleep 1
done
