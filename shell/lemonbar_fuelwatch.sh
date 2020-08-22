#!/bin/sh
# Outputs cheapest fuel today and tomorrow, allowing me to make a choice

red='#65350'
green='#99c76c'
yellow='#ffc24b'

while true; do
    today_price=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Kardinya" | rg --only-matching --pcre2 "(?<=<price>)\d{3}\.\d{1}(?=<\/price>)" | head -n 1)
    today_location=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Kardinya" | rg --only-matching --pcre2 "(?<=<trading-name>).*?(?=<\/trading-name>)" | head -n 1)
    tomorrow_price=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Kardinya&Day=tomorrow" | rg --only-matching --pcre2 "(?<=<price>)\d{3}\.\d{1}(?=<\/price>)" | head -n 1)
    tomorrow_location=$(wget -qO- "http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Kardinya&Day=tomorrow" | rg --only-matching --pcre2 "(?<=<trading-name>).*?(?=<\/trading-name>)" | head -n 1)

    #echo "F$today_location($today_price) $tomorrow_location($tomorrow_price)"
    echo "F $today_price  $tomorrow_price"
    sleep 43200
done
