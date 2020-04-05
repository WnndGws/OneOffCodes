#!/bin/python
'''Checks daily Covid-19 stats for the area and attempts to give context where needed
'''

import requests
import matplotlib.pyplot as plt

COUNTRY = "Australia"
PROVINCE = "Western Australia"

r = requests.get(f"https://corona-stats.online/{COUNTRY}?format=json&source=1")
RAW_DATA = r.json()

for i in RAW_DATA:
    if i["province"] == PROVINCE:
        WANTED_DATA = i

CASES = WANTED_DATA["confirmed"]
DAILY_CASES = WANTED_DATA["confirmedByDay"]

plt.plot(DAILY_CASES)
plt.savefig("/tmp/covid.png")
