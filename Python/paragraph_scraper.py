#!/bin/python
## Takes the arguement of a url and outputs the paragraph text from that page to a textfile

import click
import requests
from bs4 import BeautifulSoup

@click.command()
@click.option('--url')
def print_paragraph_text(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    with open('/tmp/para.txt', 'a') as f:
        for words in soup.find_all('p'):
            f.write(f'\n\n {words.text}')

@click.command()
@click.option('--url')
def save_images(url):
    s = requests.Session()
    req = s.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    for file_number, img in enumerate(soup.find_all('img'), start=1):
        img = (img['src'])
        req = s.get(img, allow_redirects=True)
        with open(f'/tmp/image{file_number}.png', 'wb') as f:
            f.write(req.content)

if __name__ == '__main__':
    #print_paragraph_text()
    save_images()
