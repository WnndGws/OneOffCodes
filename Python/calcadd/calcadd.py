#!/usr/bin/python3
## Written to add calendar events from the cli
## TODO: add a list-calendars option

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from apiclient import discovery

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "calcadd_client_secrets.json"
    APPLICATION_NAME = "Next Event"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calcadd_saved_credentials.json")
    CLIENT_SECRET_FILE = os.path.join(credential_dir, CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials


import click
import datetime
from pytz import timezone
import sys

def validate_calendar(calendar):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    page_token = None
    calendar_id = None

    calendar_list = service.calendarList().list(pageToken=page_token).execute()

    for calendar_list_entry in calendar_list['items']:
        if calendar in calendar_list_entry['summary']:
            calendar_name = calendar_list_entry['summary']
            calendar_id = calendar_list_entry['id']

    if calendar_id is None:
        print ("No calendar found with that name. Names are case sensitive")
        sys.exit(0)
    else:
        return calendar_id


@click.command()
@click.option(
    '--calendar',
    prompt=True,
    default='Personal',
    required=True,
    help='The name of the calendar you want to ad events to (Default: Personal Calendar)'
)
@click.option(
    '--title',
    prompt=True,
    required=True,
    help='The title of the event you want to add'
)
@click.option(
    '--location',
    prompt=True,
    required=True,
    help='The location of the event'
)
@click.option(
    '--description',
    prompt=True,
    required=True,
    help='The description of the event [Default: Event title]'
)
@click.option(
    '--start',
    prompt=True,
    type=click.DateTime(formats=['%Y-%m-%d %H:%M']),
    required=True,
    default=datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M"),
    help='Start time of event in format "%Y-%m-%d %H:%M" [Default: Now]'
)
@click.option(
    '--end',
    prompt=True,
    type=click.DateTime(formats=['%Y-%m-%d %H:%M']),
    default=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours = 1), "%Y-%m-%d %H:%M"),
    required=True,
    help='End time of event in format "%Y-%m-%d %H:%M" [Default: Now + 1hr]'
)
def calcadd(calendar, title, location, description, start, end):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    page_token = None

    cal_id = validate_calendar(calendar)
    event_add = {}

    tz = timezone('Australia/Perth')
    start = tz.localize(start)
    start = datetime.datetime.strftime(start, '%Y-%m-%dT%H:%M:00%z')
    end = tz.localize(end)
    end = datetime.datetime.strftime(end, '%Y-%m-%dT%H:%M:00%z')

    event_add['summary'] = title
    event_add['location'] = location
    event_add['description'] = description
    event_add['start'] = {"dateTime": start}
    event_add['end'] = {"dateTime": end}

    #breakpoint()

    service.events().insert(
        calendarId=cal_id,
        body=event_add).execute()

    print (f"Adding {title} to calendar.....")

if __name__ == "__main__":
    calcadd()
