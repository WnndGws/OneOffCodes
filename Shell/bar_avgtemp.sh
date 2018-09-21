#!/usr/bin/zsh
## Checks sensors and returns average temp

avg_temp=$(sensors | awk '{print $3}' | tail -n 5 | awk '{sum += $1} END {print sum/4}' | cut -d'.' -f1)

echo "avg: "$avg_temp"°C"
