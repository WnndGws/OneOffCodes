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

def get_next_event():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    possible_events = []
    tz = timezone('Australia/Perth')
    event_time_low = tz.localize(datetime.datetime.now() + datetime.timedelta(days=2))
    event_time_now = tz.localize((datetime.datetime.now()))
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            eventsResult = (
                service.events()
                .list(
                    calendarId=calendar_list_entry['id'],
                    timeMin=now,
                    singleEvents=True,
                    orderBy="startTime",
                    maxResults=1,
                )
                .execute()
            )
            #possible_events.append(eventsResult.get("items", []))
            event = eventsResult.get("items", [])
            if event != []:
                try:
                    event_time = event[0]['start']['dateTime']
                    event_time = datetime.datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S%z')
                except KeyError:
                    event_time = event[0]['start']['date']
                    event_time = tz.localize(datetime.datetime.strptime(event_time, '%Y-%m-%d'))
                if event_time < event_time_low and event_time > event_time_now:
                    event_time_low = event_time
                    event_title = event[0]['summary']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    event_time_low = event_time_low.strftime('%H:%M')
    print(f'{event_time_low} {event_title}')

if __name__ == "__main__":
    get_next_event()
