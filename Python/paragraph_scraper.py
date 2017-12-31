#!/bin/python
## Takes the arguement of a url and outputs the paragraph text from that page to a textfile

import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.option('--url')
def print_paragraph_text(url):
    f = open('/tmp/para.txt', 'w')
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    for words in soup.find_all('p'):
        f = open('/tmp/para.txt', 'a')
        f.write(f'\n\n {words.text}')

if __name__ == '__main__':
    print_paragraph_text()
