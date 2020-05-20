#!/usr/bin/python3
""" Re-written to scrape paragraph tags on a website
"""

import click
import requests_html


@click.command()
@click.option(
    "--url",
    prompt=True,
    help="The URL of the website to check"
)
def get_paragraph(url):
    # Get the content into my memory
    page = requests_html.HTMLSession().get(url)
    paragraphs = page.html.find('p')

    with open("/tmp/para.txt", "a") as f:
        for p in paragraphs:
            f.write(f'\n {p.text}')

if __name__ == "__main__":
    get_paragraph()
