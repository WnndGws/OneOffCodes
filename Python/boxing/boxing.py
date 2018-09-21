#!/usr/bin/python
## Script made to check when there is a middleweight+ title fight, or when 'the ring' top 10 fight

import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
from dateutil.parser import parse
import calendar
import click
import bs4
import re
import html5lib
import urllib
from unidecode import unidecode


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "boxing_client_secrets.json"
    APPLICATION_NAME = "Boxing"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "boxing_saved_credentials.json")
    CLIENT_SECRET_FILE = os.path.join(credential_dir, CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials


def scrape_wikitables():
    """Scrapes wikipedia for the list of current top boxers"""

    champURL = "https://en.wikipedia.org/wiki/List_of_current_boxing_rankings"
    page = urllib.request.urlopen(champURL)
    soup = bs4.BeautifulSoup(page, "html5lib")

    tables = soup.find_all("table", {"class": "wikitable"})
    unique_boxers = []

    for table_number in range(1, 6):
        table = tables[table_number]
        rows = table.find_all("tr")
        for row in rows:
            data = row.find_all("td")
            text = [i.text for i in data]
            for boxer_name in range(len(text)):
                if len(text[boxer_name]) > 3:
                    boxer_name = text[boxer_name].rstrip('\n')
                    boxer_name = re.findall(r"\S{3,}\ .[^\ \(]+", boxer_name)
                    if len(boxer_name) > 0:
                        if unidecode(boxer_name[0]) not in unique_boxers:
                            unique_boxers.append(unidecode(boxer_name[0]))

    unique_boxers.sort()
    return unique_boxers


def add_months(sourcedate, months):
    """Takes a sourcedate and adds months to it, outputting datetime"""

    months_fine = False
    while not months_fine:
        try:
            val = int(months)
            if not 1 < val < 12:
                months = abs(months)
                months = months - (months // 12) * 12
                if months == 0 or months == 12:
                    print(
                        f"Months must be a positive integer between 1-11, resorting to default of months=1"
                    )
                    months = 1
                else:
                    print(
                        f"Months must be a positive integer between 1-11, assuming you meant {months}"
                    )
                months_fine = True
            else:
                months_fine = True
        except ValueError:
            print("That's not an int!")
            print(
                f"Months must be a positive integer between 1-11, resorting to default of months=1"
            )
            months = 1
            months_fine = True

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


@click.command()
@click.option(
    "--start",
    default=datetime.date.today().isoformat(),
    help="Date in YYYY-MM-DD format (DEFAULT=today)",
)
@click.option(
    "--months", default=1, help="Number of months to add to start date (DEFAULT=1)"
)
@click.option("--verbose", is_flag=True, help="Will print out the results")
@click.option("--calendar", is_flag=True, help="Add results to your calendar")
def main(start, months, verbose, calendar):
    """Scrapes calendar of all fights and lists those containing any of the current top fighters"""

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    end = add_months(datetime.datetime.strptime(start, "%Y-%m-%d"), months)
    start = start + "T00:00:00Z"
    end = end.isoformat() + "T00:00:00Z"

    eventsResult = (
        service.events()
        .list(
            calendarId="6souuam0ccm9ht4jlbbp75iua8@group.calendar.google.com",
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = eventsResult.get("items", [])

    nextMonthEvents = []
    for event in events:
        eventTitle = event["summary"]
        boxer_one = re.findall(r".+?(?= vs )", eventTitle)
        boxer_two = re.findall(r"(?<=vs )(.*)(?= -)", eventTitle)
        nextMonthEvents.append(boxer_one[0])
        nextMonthEvents.append(boxer_two[0])

    unique_boxers = scrape_wikitables()
    boxer_i_care_about = set(unique_boxers).intersection(nextMonthEvents)

    if verbose:
        for event in events:
            eventTitle = event["summary"]
            boxer_one = re.findall(r".+?(?= vs )", eventTitle)
            boxer_two = re.findall(r"(?<=vs )(.*)(?= -)", eventTitle)
            if len(set(boxer_one).intersection(boxer_i_care_about)) > 0:
                for item in ["summary", "location", "start"]:
                    click.echo(f"{item}: {event[item]}")
                click.echo("\n")
            elif len(set(boxer_two).intersection(boxer_i_care_about)) > 0:
                for item in ["summary", "location", "start"]:
                    click.echo(f"{item}: {event[item]}")
                click.echo("\n")

    if calendar:
        for event in events:
            eventTitle = event["summary"]
            boxer_one = re.findall(r".+?(?= vs )", eventTitle)
            boxer_two = re.findall(r"(?<=vs )(.*)(?= -)", eventTitle)
            if len(set(boxer_one).intersection(boxer_i_care_about)) > 0:
                newEvent = {}
                reminderEvent = {}
                for item in [
                    "summary",
                    "location",
                    "description",
                    "start",
                    "end",
                    "description",
                ]:
                    newEvent[item] = event[item]
                reminderEvent["summary"] = f'REMINDER: Download {event["summary"]}'
                reminderEvent["start"] = {
                    "dateTime": f'{datetime.datetime.strftime(parse(event["start"]["dateTime"]) + datetime.timedelta(days=1), "%Y-%m-%dT19:00:00%z")}'
                }
                reminderEvent["end"] = {
                    "dateTime": f'{datetime.datetime.strftime(parse(event["end"]["dateTime"]) + datetime.timedelta(days=1), "%Y-%m-%dT20:00:00%z")}'
                }
                reminderEvent["description"] = f'{event["description"]}'
                service.events().insert(
                    calendarId="nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com",
                    body=newEvent,
                ).execute()
                service.events().insert(
                    calendarId="nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com",
                    body=reminderEvent,
                ).execute()
                click.echo("Adding event(s) to calendar......")
            elif len(set(boxer_two).intersection(boxer_i_care_about)) > 0:
                newEvent = {}
                reminderEvent = {}
                for item in [
                    "summary",
                    "location",
                    "description",
                    "start",
                    "end",
                    "description",
                ]:
                    newEvent[item] = event[item]
                reminderEvent["summary"] = f'REMINDER: Download {event["summary"]}'
                reminderEvent["start"] = {
                    "dateTime": f'{datetime.datetime.strftime(parse(event["start"]["dateTime"]) + datetime.timedelta(days=1), "%Y-%m-%dT19:00:00%z")}'
                }
                reminderEvent["end"] = {
                    "dateTime": f'{datetime.datetime.strftime(parse(event["end"]["dateTime"]) + datetime.timedelta(days=1), "%Y-%m-%dT20:00:00%z")}'
                }
                reminderEvent["description"] = f'{event["description"]}'
                service.events().insert(
                    calendarId="nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com",
                    body=newEvent,
                ).execute()
                service.events().insert(
                    calendarId="nvorn96ej1f3i5h597eqvrimpo@group.calendar.google.com",
                    body=reminderEvent,
                ).execute()
                click.echo("Adding event(s) to calendar......")

    return boxer_i_care_about


if __name__ == "__main__":
    main()
