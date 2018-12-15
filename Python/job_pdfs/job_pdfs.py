#!/usr/bin/python3
''' Use to find pdfs on job websites
'''

from bs4 import BeautifulSoup
from requests import get
from fake_useragent import UserAgent
import click

UA = UserAgent()


def download_pdfs(test_url):
    ''' Takes a url and sees if it ends in pdf
    '''

    if test_url.endswith(('.pdf')):
        pdf_name = test_url.split('/')[-1]
        pdf_file = get(test_url).content
        #print(test_url)
        #print(pdf_name)

        try:
            open(pdf_name, 'r')
        except IOError:
            with open(pdf_name, 'wb') as f:
                f.write(pdf_file)

def lovely_soup(url):
    ''' Takes URL and returns the BS from it
    '''

    header = {'User-Agent': UA.chrome}
    ret = get(url, headers=header)
    cet = ret.text
    return BeautifulSoup(cet, 'lxml')

@click.command()
@click.option(
    "--scrape-url",
    prompt=True,
    help="The URL of the website to check"
    )
def find_links(scrape_url):
    ''' Checks page source for pdfs
    '''

    soup = lovely_soup(scrape_url)
    links = soup.findAll('a')

    for link in links:
        try:
            download_pdfs(link['href'])
        except:
            pass

if __name__ == "__main__":
    find_links()
