#!/bin/sh
# Outputs cheapest fuel today and tomorrow, allowing me to make a choice

while true; do
    raw_output_today=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Bibra%20Lake")
    raw_output_tomorrow=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Bibra%20Lake&Day=tomorrow")
    today_price=$(printf "%s" "$raw_output_today" | rg --only-matching --pcre2 "(?<=<price>)\d{3}\.\d{1}(?=<\/price>)" | head -n 1)
    #today_location=$(printf "%s" "$raw_output_today" | rg --only-matching --pcre2 "(?<=<trading-name>).*?(?=<\/trading-name>)" | head -n 1)
    tomorrow_price=$(printf "%s" "$raw_output_tomorrow" | rg --only-matching --pcre2 "(?<=<price>)\d{3}\.\d{1}(?=<\/price>)" | head -n 1)
    #tomorrow_location=$(printf "%s" "$raw_output_tomorrow" | rg --only-matching --pcre2 "(?<=<trading-name>).*?(?=<\/trading-name>)" | head -n 1)

    #echo "F$today_location($today_price) $tomorrow_location($tomorrow_price)"
    [ -z "$tomorrow_price" ] && echo "F $today_price" || echo "F $today_price  $tomorrow_price"
    sleep 43200
done
