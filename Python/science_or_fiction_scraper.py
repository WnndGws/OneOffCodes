#!/usr/bin/python3
''' This script will scrape the SGU website for Science or Fiction games
Displays them all for my use
'''

import random
import requests_html

import click

RANDOM_EPISODE = random.randint(1, 800)

@click.command()
@click.option(
    "--episode",
    prompt=True,
    default=RANDOM_EPISODE,
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
    session = requests_html.HTMLSession()
    r = session.get(url)

    # Find just the list items I want
    item_list = []
    items = r.html.find('li.science-fiction__item')
    for item in items:
        text = item.find('p')[0].full_text
        answer = item.find('span.quiz__answer')[0].full_text
        item_number = item.find('span')[0].full_text
        if answers:
            item_list.append(f'{item_number} - {answer}: {text}')
        else:
            item_list.append(f'{item_number} - {text}')

    for item in item_list:
        print(f'{item}\n')

if __name__ == "__main__":
    get_science_or_fiction()
