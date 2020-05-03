#!/usr/bin/python3
## This script will scrape the SGU website for Science or Fiction games, and display them all for my use

import click
from itertools import cycle
import random
import re
import requests_html
from lxml import html

random_episode = random.randint(1,700)

@click.command()
@click.option(
    "--episode",
    prompt=True,
    default=random_episode,
    help="Episode number between 1 and 700"
    )
@click.option(
    "--answers",
    is_flag=True,
    help="Flag to show answers")

def get_science_or_fiction(episode, answers):
    # The url I want to scrape
    url = f"https://www.theskepticsguide.org/podcasts/episode-{episode}"

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
    items_list = []
    n = 1

    if answers:
        for i in items:
            if re.findall(r".*Science", i):
                items_dict[f"Science0{n}"] = next_item
                n += 1
            if re.findall(r".*Fiction", i):
                items_dict["Fiction"] = next_item
            next_item = next(items_cycle)
        print (items_dict)
    else:
        for i in items:
            if re.findall(r".*Science", i):
                items_list.append(next_item)
            if re.findall(r".*Fiction", i):
                items_list.append(next_item)
            next_item = next(items_cycle)
        for item in items_list:
            print (f'{item}\n')


if __name__ == "__main__":
    get_science_or_fiction()
