#!/usr/bin/python
## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

from __future__ import print_function
from apiclient import discovery
from bs4 import BeautifulSoup
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
import calendar
import click
import datetime
import httplib2
import optparse
import os
import re
import sys
import urllib.request

def scrape_wikitables():
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
    return unique_boxers

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'boxing2.0_client_id.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('/home/wynand/.credentials/client_secrets_boxing2.0.json', scope='https://www.googleapis.com/auth/calendar')
        flow.user_agent = 'Boxing2.0'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

#def parse_args():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('--start', action="store", dest="start", default=datetime.date.today().isoformat(), help='Date in YYYY-MM-DD format')
    #parser.add_argument('--end', action="store", dest="end", default=add_months(datetime.date.today(), 1), help='Date in YYYY-MM-DD format')
    #args = parser.parse_args()
    #return args

@click.group()
def run_list_important():
    pass

@run_list_important.command()
@click.option('--start', default=datetime.date.today().isoformat(), help="Date in YYYY-MM-DD format")
@click.option('--end', default=add_months(datetime.date.today(), 1), help="Date in YYYY-MM-DD format")
def list_important(start, end):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    start = start + 'T00:00:00Z' # 'Z' indicates UTC time
    if type(end) == 'str':
        end = end + 'T00:00:00Z'
    else:
        end = end.isoformat() + 'T00:00:00Z'

    eventsResult = service.events().list(
        calendarId='1krp7iu4q65i0qt6eagdjj5ucs@group.calendar.google.com', timeMin=start, timeMax=end, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    nextMonthEvents = []
    for event in events:
        eventTitle = event['summary']
        boxer_one = re.findall(r'.+?(?= vs )', eventTitle)
        boxer_two = re.findall(r'(?<=vs )(.*)(?= -)', eventTitle)
        nextMonthEvents.append(boxer_one[0])
        nextMonthEvents.append(boxer_two[0])

    unique_boxers = scrape_wikitables()
    boxer_i_care_about = set(unique_boxers).intersection(nextMonthEvents)
    return boxer_i_care_about
    print(boxer_i_care_about)

def add_to_cal():
    list_important()
    for event in events:
        eventTitle = event['summary']
        boxer_one = re.findall(r'.+?(?= vs )', eventTitle)
        boxer_two = re.findall(r'(?<=vs )(.*)(?= -)', eventTitle)
        if len(set(boxer_one).intersection(boxer_i_care_about)) > 0:
            newEvent = {}
            for item in ['summary', 'location', 'description', 'start', 'end', 'description']:
                newEvent[item] = event[item]
            service.events().insert(calendarId='nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com', body=newEvent).execute()
        elif len(set(boxer_two).intersection(boxer_i_care_about)) > 0:
            service.events().insert(calendarId='nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com', body=newEvent).execute()

LIST_UPCOMING = click.CommandCollection(sources=[run_list_important])

if __name__ == '__main__':
    LIST_UPCOMING()
