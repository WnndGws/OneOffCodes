#!/usr/bin/python
## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
import calendar
import click
import bs4
import re
import html5lib
import urllib

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'boxing3.1_client_id.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow_path = os.path.join(home_dir, '.credentials/client_secrets_boxing3.1.json')
        flow = client.flow_from_clientsecrets(flow_path, scope='https://www.googleapis.com/auth/calendar')
        flow.user_agent = 'Boxing'
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def scrape_wikitables():
    """Scrapes wikipedia for the list of current top boxers"""

    champURL = 'https://en.wikipedia.org/wiki/List_of_current_boxing_rankings'
    page = urllib.request.urlopen(champURL)
    soup = bs4.BeautifulSoup(page, "html5lib")

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

def add_months(sourcedate,months):
    """Takes a sourcedate and adds months to it, outputting datetime"""

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return datetime.date(year,month,day)

@click.group()
def run_list_important():
    pass

@run_list_important.command()
@click.option('--start', default=datetime.date.today().isoformat(), help="Date in YYYY-MM-DD format (DEFAULT=today)")
@click.option('--months', default=1, help="Number of months to add to start date (DEFAULT=1)")
@click.option('--verbose', is_flag=True, help="Will print out the results")
@click.option('--calendar', is_flag=True, help="Add results to your calendar")
def list_important(start, months, verbose, calendar):
    """Scrapes calendar of all fights and lists those containing any of the current top fighters"""

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    end = add_months(datetime.datetime.strptime(start, '%Y-%m-%d'), months)
    start = start + 'T00:00:00Z'
    end = end.isoformat() + 'T00:00:00Z'

    eventsResult = service.events().list(calendarId='1krp7iu4q65i0qt6eagdjj5ucs@group.calendar.google.com', timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()
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

    if verbose:
        for event in events:
            eventTitle = event['summary']
            boxer_one = re.findall(r'.+?(?= vs )', eventTitle)
            boxer_two = re.findall(r'(?<=vs )(.*)(?= -)', eventTitle)
            if len(set(boxer_one).intersection(boxer_i_care_about)) > 0:
                for item in ['summary', 'location', 'start']:
                    click.echo(f'{item}: {event[item]}')
                click.echo('\n')
            elif len(set(boxer_two).intersection(boxer_i_care_about)) > 0:
                for item in ['summary', 'location', 'start']:
                    click.echo(f'{item}: {event[item]}')
                click.echo('\n')

    if calendar:
        for event in events:
            eventTitle = event['summary']
            boxer_one = re.findall(r'.+?(?= vs )', eventTitle)
            boxer_two = re.findall(r'(?<=vs )(.*)(?= -)', eventTitle)
            if len(set(boxer_one).intersection(boxer_i_care_about)) > 0:
                newEvent = {}
                for item in ['summary', 'location', 'description', 'start', 'end', 'description']:
                    newEvent[item] = event[item]
                service.events().insert(calendarId='nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com', body=newEvent).execute()
                click.echo('Adding event(s) to calendar......')
            elif len(set(boxer_two).intersection(boxer_i_care_about)) > 0:
                newEvent = {}
                for item in ['summary', 'location', 'description', 'start', 'end', 'description']:
                    newEvent[item] = event[item]
                service.events().insert(calendarId='nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com', body=newEvent).execute()
                click.echo('Adding event(s) to calendar......')

    return boxer_i_care_about

LIST_UPCOMING = click.CommandCollection(sources=[run_list_important])

if __name__ == '__main__':
    LIST_UPCOMING()
