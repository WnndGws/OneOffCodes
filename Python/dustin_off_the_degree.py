#!/bin/python3
# Used to scrape episode numbers and topic from podcast show notes

import json
import re
import requests
from bs4 import BeautifulSoup

ep_dict = {}

def download_mp3(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def iterate_through():
    for n in range(130, 250):
        url = f'http://atheistnomads.com/{n}'
        print(url)
        req = requests.get(url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.content, "html.parser")
            para = soup.find_all('p')
            for words in para:
                if re.match('.*(dustin).*(degree).*', words.text, re.IGNORECASE) is not None:
                    ep_dict[n] = f'{words.text}\n'
                    url = f'http://traffic.libsyn.com/forcedn/atheistnomads/atheist_nomads_{n}.mp3'
                    download_mp3(url)
    with open('dustin_degree.txt', 'w') as file:
        file.write(json.dumps(ep_dict))

if __name__ == '__main__':
    iterate_through()
