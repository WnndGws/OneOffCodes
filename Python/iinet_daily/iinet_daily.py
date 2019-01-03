#!/usr/bin/python3
## Get iinet Usage

import configparser
from requests import get
from datetime import datetime


'''To get token:
1) %load in ipython
2) set username and password as variables
3) run 'get("https://toolbox.iinet.net.au/cgi-bin/api.cgi",
               params={"_USERNAME": user, "_PASSWORD": password}).json()'
'''

config = configparser.ConfigParser()
config.read('/home/wynand/.config/polybar_credentials/iinet.ini')
token = config.get('Credentials', 'token')
username = config.get('Credentials', 'username')

url = f"https://toolbox.iinet.net.au/cgi-bin/api.cgi?Usage&_TOKEN={token}&_SERVICE={username}"
data = get(url).json()

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def get_remaining_peak():
    peak_used = data["response"]["usage"]["traffic_types"][0]["used"]
    peak_allocation = data["response"]["usage"]["traffic_types"][0]["allocation"]
    days_remaining = data["response"]["quota_reset"]['days_remaining']
    allowed_peak = (peak_allocation-peak_used)/days_remaining
    allowed_peak = humansize(allowed_peak)

    return allowed_peak

def get_remaining_offpeak():
    offpeak_used = data["response"]["usage"]["traffic_types"][1]["used"]
    offpeak_allocation = data["response"]["usage"]["traffic_types"][1]["allocation"]
    days_remaining = data["response"]["quota_reset"]['days_remaining']
    allowed_offpeak = (offpeak_allocation-offpeak_used)/days_remaining
    allowed_offpeak = humansize(allowed_offpeak)

    return allowed_offpeak

def get_daily_usage_peak():
    today = datetime.now().strftime("%Y%m%d")
    for i in data["response"]["usage"]["data"]:
        if str(i["period"]) == today:
            peak_used = humansize(i["types"][0]["value"])
    return peak_used

def get_daily_usage_offpeak():
    today = datetime.now().strftime("%Y%m%d")
    for i in data["response"]["usage"]["data"]:
        if str(i["period"]) == today:
            offpeak_used = humansize(i["types"][1]["value"])
    return offpeak_used

if __name__ == "__main__":
    peak_used = get_daily_usage_peak()
    offpeak_used = get_daily_usage_offpeak()
    peak_allowed = get_remaining_peak()
    offpeak_allowed = get_remaining_offpeak()

    print (f' Offpeak: {offpeak_used}/{offpeak_allowed} |  Peak: {peak_used}/{peak_allowed}')
    #print(f'Peak used today: {peak_used}\nPeak Allowed per day: {peak_allowed}\n\n Offpeak used today: {offpeak_used}\n Offpeak Allowed per day: {offpeak_allowed}')
