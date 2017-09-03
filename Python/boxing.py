## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

from bs4 import BeautifulSoup
import urllib.request

# Step 01-import list of names I care about from wiki
champWikiURL = 'https://en.wikipedia.org/wiki/List_of_current_world_boxing_champions'
page = urllib.request.urlopen(champWikiURL)
soup = BeautifulSoup(page)
champTables = soup.findAll("table", {"class" : "wikitable"})

print(champTables)
## https://github.com/rocheio/wiki-table-scrape/blob/master/wikitablescrape.py
