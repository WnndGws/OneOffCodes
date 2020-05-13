#!/usr/bin/python3
'''Written to add calendar events from the cli
    TODO: add a list-calendars option'''

import os
import datetime
import sys
import httplib2
import click
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import discovery
from pytz import timezone

class EndOption(click.Option):
    def get_default(self, ctx):
        default = super().get_default(ctx)
        if default is None:
            default = ctx.params['start'] + datetime.timedelta(hours=1)
        return default


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    scopes = "https://www.googleapis.com/auth/calendar"
    client_secret_file = "calcadd_client_secrets.json"
    application_name = "Next Event"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calcadd_saved_credentials.json")
    client_secret_file = os.path.join(credential_dir, client_secret_file)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials


CREDENTIALS = get_credentials()
HTTP = CREDENTIALS.authorize(httplib2.Http())
SERVICE = discovery.build("calendar", "v3", http=HTTP)
PAGE_TOKEN = None

def validate_calendar(calendar):
    '''Function to check if input calendar string is a calendar the api has access to'''

    calendar_id = None

    calendar_list = SERVICE.calendarList().list(pageToken=PAGE_TOKEN).execute()

    for calendar_list_entry in calendar_list['items']:
        if calendar in calendar_list_entry['summary']:
            calendar_id = calendar_list_entry['id']

    if calendar_id is None:
        print("No calendar found with that name. Names are case sensitive")
        sys.exit(0)
    else:
        return calendar_id

def print_calendars(ctx, param, value):
    '''Function to print all available calendars'''

    #Check if value is passed in, otherwise will always run
    if not value or ctx.resilient_parsing:
        return

    #Actual print function
    calendar_list = SERVICE.calendarList().list(pageToken=PAGE_TOKEN).execute()
    for calendar_list_entry in calendar_list['items']:
        print(calendar_list_entry["summary"])
    sys.exit(0)

@click.command()
@click.option(
    '--print-calendars',
    is_flag=True,
    callback=print_calendars,
    expose_value=False,
    is_eager=True
)
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
    cls=EndOption,
    prompt=True,
    type=click.DateTime(formats=['%Y-%m-%d %H:%M']),
    required=True,
    help='End time of event in format "%Y-%m-%d %H:%M" [Default: Now + 1hr]'
)
def calcadd(calendar, title, location, description, start, end):
    cal_id = validate_calendar(calendar)
    event_add = {}

    time_zone = timezone('Australia/Perth')
    start = time_zone.localize(start)
    start = datetime.datetime.strftime(start, '%Y-%m-%dT%H:%M:00%z')
    end = time_zone.localize(end)
    end = datetime.datetime.strftime(end, '%Y-%m-%dT%H:%M:00%z')

    event_add['summary'] = title
    event_add['location'] = location
    event_add['description'] = description
    event_add['start'] = {"dateTime": start}
    event_add['end'] = {"dateTime": end}

    #breakpoint()

    SERVICE.events().insert(
        calendarId=cal_id,
        body=event_add).execute()

    print(f"Adding {title} to calendar.....")

if __name__ == "__main__":
    calcadd()
