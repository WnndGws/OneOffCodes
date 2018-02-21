#!/bin/python
## Takes the arguement of a url and outputs the paragraph text from that page to a textfile

import re
import requests
import sys

from bs4 import BeautifulSoup

## Collect command-line arguements from input
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def scrape_content(url):
    s = requests.Session()
    req = s.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    with open('/tmp/para.txt', 'a') as f:
        for words in soup.findAll('p'):
            f.write(f'\n\n {words.text}')

if __name__ == '__main__':
    from sys import argv
    myargs = getopts(argv)
    if '--url' in myargs:
        url = myargs['--url']
    scrape_content(url)