#!/usr/bin/python3
## This script will scrape the SGU website for Science or Fiction games, and display them all for my use

from itertools import cycle
import re
import requests_html
from lxml import html

# The url I want to scrape
url = "https://www.theskepticsguide.org/sgu/675"

# Get the content into my memory
page = requests_html.HTMLSession().get(url)
tree = html.fromstring(page.content)

# Inspect element you want, copy Xpath to find this string
items = tree.xpath("//html/body/section[@id='body']/div/div/div/div/div[@class='podcast-segments']/div[@class='podcast-segment']/ul/li//text()")

# Remove the million " " strings in the list
items = [x for x in items if x != " "]

# just moves last item to first place, and each element down one
items_cycle = cycle(items)
next_item = next(items_cycle)
next_item = next(items_cycle)
items_dict = {}
n = 1

for i in items:
    if re.findall(r".*Science", i):
        items_dict[f"Science0{n}"] = next_item
        n += 1
    if re.findall(r".*Fiction", i):
        items_dict["Fiction"] = next_item
    next_item = next(items_cycle)

print (items_dict)
