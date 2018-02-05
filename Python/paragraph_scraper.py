#!/bin/python
## Takes the arguement of a url and outputs the paragraph text from that page to a textfile

import click
import re
import requests
from bs4 import BeautifulSoup

@click.command(
    context_settings=dict(ignore_unknown_options=True,
                          allow_extra_args=True,
                          resilient_parsing=True))
@click.option('--url_para')
def print_paragraph_text(url_para):
    req = requests.get(url_para)
    soup = BeautifulSoup(req.content, "html.parser")
    with open('/tmp/para.txt', 'a') as f:
        for words in soup.findAll('p'):
            f.write(f'\n\n {words.text}')

@click.command(
    context_settings=dict(ignore_unknown_options=True,
                          allow_extra_args=True,
                          resilient_parsing=True))
@click.option('--url_image')
def save_images(url_image):
    s = requests.Session()
    req = s.get(url_image)
    soup = BeautifulSoup(req.content, "html.parser")
    for file_number, img in enumerate(soup.findAll('img'), start=1):
        img = (img['src'])
        if re.match(r'(http).*', img) is not None:
            req = s.get(img, allow_redirects=True)
            with open(f'/tmp/image{file_number}.png', 'wb') as f:
                f.write(req.content)

if __name__ == '__main__':
    print_paragraph_text()
    save_images()
