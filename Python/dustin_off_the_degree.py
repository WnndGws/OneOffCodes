#!/bin/python3
# Used to scrape episode numbers and topic from podcast show notes

import json
import re
import requests
from bs4 import BeautifulSoup

ep_dict = {}

def itterate_through():
    for n in range(1, 300):
        url = f'http://atheistnomads.com/{n}'
        print(url)
        req = requests.get(url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.content, "html.parser")
            para = soup.find_all('p')
            for words in para:
                if re.match('.*(dustin).*(degree).*', words.text, re.IGNORECASE) is not None:
                    ep_dict[n] = words.text
    with open('dustin_degree.txt', 'w') as file:
        file.write(json.dumps(ep_dict))

if __name__ == '__main__':
    itterate_through()
