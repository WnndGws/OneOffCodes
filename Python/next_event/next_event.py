#!/usr/bin/python3
## Written to replace the next_event.sh. Checks google calendar for next event and displays it nicely

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
from apiclient import discovery
import httplib2
from pytz import timezone

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

def print_events():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # 'Z' needed for calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    # TODO: add click option for this
    tz = timezone('Australia/Perth')
    # Need to change times to non-naive
    event_time_low = tz.localize(datetime.datetime.now() + datetime.timedelta(days=2))
    event_time_high = tz.localize(datetime.datetime.now() + datetime.timedelta(hours=24))
    event_time_now = tz.localize((datetime.datetime.now()))
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
        event = eventsResult.get("items", [])

        i = 0
        size_of_list = len(event)
        #breakpoint()
        while i < size_of_list:
            if event != []:
                event_title = event[i]['summary']
                try:
                    event_time = event[i]['start']['dateTime']
                    event_time = datetime.datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S%z')
                except KeyError:
                    event_time = event[i]['start']['date']
                    event_time = tz.localize(datetime.datetime.strptime(event_time, '%Y-%m-%d'))

                print(f"{event_time}: {event_title}")

            i += 1

def get_next_event():
    """ Loops to find how many calendars, then gets next event for each calendar, but only keeps the next one
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # 'Z' needed for calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    # TODO: add click option for this
    tz = timezone('Australia/Perth')
    # Need to change times to non-naive
    event_time_low = tz.localize(datetime.datetime.now() + datetime.timedelta(days=2))
    event_time_high = tz.localize(datetime.datetime.now() + datetime.timedelta(hours=24))
    event_time_now = tz.localize((datetime.datetime.now()))
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
                    event_time = event[0]['start']['dateTime']
                    event_time = datetime.datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S%z')
                except KeyError:
                    event_time = event[0]['start']['date']
                    event_time = tz.localize(datetime.datetime.strptime(event_time, '%Y-%m-%d'))
                if event_time < event_time_low and event_time > event_time_now and event_time < event_time_high:
                    event_time_low = event_time
                    event_title = event[0]['summary']
                elif event_time == event_time_low:
                    event_title = event[0]['summary'][:9] + " Multiple events"
            i += 1

    #page_token = calendar_list.get('nextPageToken')
    #if not page_token:
        #break

    event_time_low = event_time_low.strftime('%H:%M')
    try:
        print(f'{event_time_low} {event_title}')
    except:
        pass

if __name__ == "__main__":
    get_next_event()
    #print_events()
