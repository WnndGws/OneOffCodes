## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import urllib.request

# Step 01-import list of names I care about from wiki
#champURL = 'http://fightnews.com/rankings-2'
champURL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
page = urllib.request.urlopen(champURL)
soup = BeautifulSoup(page, "lxml")

# Find the names of each sanctioning body
sanctioningBodies = [td.getText() for td in soup.findAll('tr', limit=4)[3].findAll('td')]
# I am finding the first 4 table rows, then reading the 4th row, in that i am finding
# the td of that row, and using list comprehension to print the contents, giving me
# table headers

table = soup.find_all('table')
k = 3
all_boxers = []

while k < 136:
    tableRows = table.find_all('tr')[k:k+1]
    for tr in tableRows:
        td = tr.find_all('td')
        row = [i.text for i in td]
    ## I now lists, where each list is a row of the table

    if len(row[0].split('\n'))<15:
        for boxer_in_row in row:
            boxer_name = re.findall(r'[a-zA-Z]{3,}\ [a-zA-Z]+', boxer_in_row)
            if len(boxer_name) > 0:
                all_boxers.append(boxer_name[0])
        k += 1
    else:
        rank = []
        i = 0
        while i < len(row[0].split('\n')):
            j = 0
            boxers = []
            while j < len(row):
                boxer_in_row = row[j].split('\n')[i]
                boxers.append(boxer_in_row)
                boxer_name = re.findall(r'[a-zA-Z]{3,}\ [a-zA-Z]+', boxer_in_row)
                if len(boxer_name) > 0:
                    all_boxers.append(boxer_name[0])
                j += 1
            rank.append(boxers)
            i += 1
        ## Now have 'rank' which is a list of the number i ranked in each sanctioning body

        df = pd.DataFrame(rank, columns=sanctioningBodies)
        ## Now have a DataFrame with 4 columns and the ranks in each
        #print(df.head(3))

        k += 1

unique_boxers = []
for boxer in all_boxers:
    if boxer not in unique_boxers:
        unique_boxers.append(boxer)

print(unique_boxers)
## Now have a list of boxer names that i care about

## Next step is import events from google calendar and scrape them
##https://gist.github.com/wassname/5b10774dfcd61cdd3f28
    ## https://github.com/rocheio/wiki-table-scrape/blob/master/wikitablescrape.py
    ## http://savvastjortjoglou.com/nba-draft-part01-scraping.html
