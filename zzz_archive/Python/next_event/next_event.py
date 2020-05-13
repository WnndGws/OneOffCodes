#!/usr/bin/python3
## Written to replace the next_event.sh. Checks google calendar for next event and displays it nicely

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "next_event_client_secrets.json"
    APPLICATION_NAME = "Next Event"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "next_event_saved_credentials.json")
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
from apiclient import discovery
import httplib2
from pytz import timezone
import re

@click.command()
@click.option(
    '--print-all',
    is_flag=True,
    default=False,
    help="Flag to print all events found (Default = False)"
)
@click.option(
    '--location',
    default='Australia/Perth',
    help="The timezone you are living in (Default = Australia/Perth)"
)
@click.option(
    '--allday-events',
    is_flag=True,
    default=False,
    help="Flag to include allday events in output (Default = False)"
)

def get_next_event(print_all, location, allday_events):
    """ Loops to find how many calendars, then gets next event for each calendar, but only keeps the next one
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # 'Z' needed for calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.date.today().isoformat()
    today = datetime.datetime.strptime(today, "%Y-%m-%d")

    tz = timezone(location)
    # Need to change times to non-naive
    event_time_low = tz.localize(datetime.datetime.now() + datetime.timedelta(days=5))
    event_end_low = event_time_low
    event_time_high = tz.localize(datetime.datetime.now() + datetime.timedelta(hours=24))
    event_time_now = tz.localize((datetime.datetime.now()))
    event_title_low = None
    page_token = None

    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    # Get next event in each calendar
    for calendar_list_entry in calendar_list['items']:
        eventsResult = (
            service.events()
            .list(
                calendarId=calendar_list_entry['id'],
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
                maxResults=2,
            )
            .execute()
        )
        #possible_events.append(eventsResult.get("items", []))
        event = eventsResult.get("items", [])

        #breakpoint()

        i = 0
        size_of_list = len(event)
        while i < size_of_list:
            if event != []:
                try:
                    event_time = event[i]['start']['dateTime']
                    if event_time[-1] == 'Z':
                        #time_diff = int(event_time[-8])
                        event_time = datetime.datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%SZ")
                        #event_time = event_time + datetime.timedelta(hours = (8-time_diff))
                        event_time = event_time + datetime.timedelta(hours = 8)
                        event_time = tz.localize(event_time)
                        #event_time = datetime.datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S%z')
                    else:
                        event_time = datetime.datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S%z')

                    event_end = event[i]['end']['dateTime']
                    if event_end[-1] == 'Z':
                        event_end = datetime.datetime.strptime(event_end, '%Y-%m-%dT%H:%M:%SZ')
                        event_end = event_end + datetime.timedelta(hours = 8)
                        event_end = tz.localize(event_end)
                    else:
                        event_end = datetime.datetime.strptime(event_end, '%Y-%m-%dT%H:%M:%S%z')

                    event_title = event[i]['summary']

                    if print_all:
                        print(f'{calendar_list_entry}: {event_time} to {event_end}: {event_title}')
                    if event_end < event_end_low and event_time < event_time_high:
                        event_end_low = event_end
                        event_time_low = event_time
                        event_title_low = event[i]['summary']
                        if event_time < event_time_now < event_end:
                            i = len(event)
                    elif event_time == event_time_low:
                        event_title_low = event[i]['summary'][:9] + " Multiple events"
                except KeyError:
                    if allday_events:
                        event_time = event[i]['start']['date']
                        event_time = datetime.datetime.strptime(event_time, '%Y-%m-%d')
                        event_end = tz.localize(event_time)
                        event_title = event[i]['summary']
                        if event_title_low is None and event_time == today:
                            event_title_low = event_title
                            event_time_low = tz.localize(event_time)
                        if print_all:
                            print(f'{event_time}: {event_title}')
                    else:
                        break

            i += 1

    #breakpoint()
    try:
        if event_time_low.strftime('%H:%M') == '00:00':
            event_time_low = "Today:"
        elif event_time_low < event_time_now < event_end:
            event_time_low = "Now:"
        else:
            event_time_low = event_time_low.strftime('%H:%M')

        if 'Forecast' in event_title_low:
            forecast = re.findall(r'[0-9](?:(?!\)).)*', event_title_low)
            event_title_low = 'Forecast ' + forecast[0].replace(' | ', ' … ')

        if len(event_title_low) > 25:
            event_title_low = event_title_low[:22] + '……'

        print(f'{event_time_low} {event_title_low}')
    except:
        pass

if __name__ == "__main__":
    get_next_event()
