## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

from bs4 import BeautifulSoup
import re
import urllib.request

champURL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
page = urllib.request.urlopen(champURL)
soup = BeautifulSoup(page, "lxml")

tables = soup.find_all('table', { "class" : "wikitable"})
unique_boxers = []

for table_number in range(2,6):
    table = tables[table_number]
    rows = table.find_all('tr')
    for row in rows:
        data = row.find_all('td')
        text = [i.text for i in data]
        for boxer_name in range(len(text)):
            if len(text[boxer_name]) > 3:
                boxer_name = re.findall(r'\S{3,}\ .[^\ \(]+', text[boxer_name])
                if len(boxer_name) > 0:
                    if boxer_name[0] not in unique_boxers:
                        unique_boxers.append(boxer_name[0])

unique_boxers.sort()
print(unique_boxers)
