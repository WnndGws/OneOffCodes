## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

from bs4 import BeautifulSoup
import urllib.request

# Step 01-import list of names I care about from wiki
champURL = 'http://fightnews.com/rankings-2'
page = urllib.request.urlopen(champURL)
soup = BeautifulSoup(page, "lxml")

# Find the names of each sanctioning body
sanctioningBodies = [td.getText() for td in soup.findAll('tr', limit=4)[3].findAll('td')]
# I am finding the first 4 table rows, then reading the 4th row, in that i am finding
# the td of that row, and using list comprehension to print the contents, giving me
# table headers

table = soup.find('table')
tableRows = table.find_all('tr')
for tr in tableRows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print (row)
## I now lists, where each list is a row of the table


## https://github.com/rocheio/wiki-table-scrape/blob/master/wikitablescrape.py
## http://savvastjortjoglou.com/nba-draft-part01-scraping.html
