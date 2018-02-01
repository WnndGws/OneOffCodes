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
    file_number = 1
    s = requests.Session()
    req = s.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    for img in soup.find_all('img'):
        img = (img['src'])
        try:
            req = s.get(img, allow_redirects=True)
            print(f'/tmp/image{file_number}')
            with open(f'/tmp/image{file_number}.png', 'wb') as f:
                f.write(req.content)
            file_number += 1
        except:
            pass

if __name__ == '__main__':
    print_paragraph_text()
    #save_images()
