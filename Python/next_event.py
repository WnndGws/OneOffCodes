#!/usr/bin/python3
'''Written to replace the next_event2.
Checks google calendar for next event and displays it nicely
'''

import datetime
import os

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import discovery
import httplib2
import humanize
from pytz import timezone

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    scopes = "https://www.googleapis.com/auth/calendar"
    client_secret_file = "nextevent2clientsecrets.json"
    application_name = "Next Event 2.0"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".cache/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "nextevent_savedcredentials.json")
    client_secret_file = os.path.join(credential_dir, client_secret_file)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_file, scopes)
        flow.user_agent = application_name
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials

def getnextevent():
    """ Loops through all calendars and prints the next even in each one """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # 'Z' needed for calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    # Needed to change times to non-naive
    location = 'Australia/Perth'
    tz = timezone(location)
    page_token = None

    calendar_list = service.calendarList().list(pageToken=page_token).execute()

    # Get next event in each calendar and add it to 'event_list'
    event_list = []
    for calendar_list_entry in calendar_list['items']:
        event_result = (
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
        event = event_result.get("items", [])
        if event != []:
            event_list.extend(event)

    # Set far into future lowest start to begin with
    lowest_start_time = datetime.datetime(2050, 1, 1)
    for event in event_list:
        if "dateTime" in event["start"]:
            try:
                # Need to strp info into a datetime, then add UTC offset, so can have all times in local time
                start_time = datetime.datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ") + tz.utcoffset(datetime.datetime.now())
            except:
                # If dateTime already includes offset, then strip the +08
                # Doesnt affect output, just creates naive datetime
                start_time = datetime.datetime.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%S+08:00")
            start_time_test = start_time
        elif "date" in event["start"]:
            start_time = datetime.datetime.strptime(event["start"]["date"], "%Y-%m-%d")
            # When making comparisons, an All day event only comes 1st if it there is nothing else that day
            start_time_test = start_time + datetime.timedelta(seconds=86399)
        if start_time_test < lowest_start_time:
            lowest_start_time = start_time
            lowest_title = event["summary"]

    print(f'{humanize.naturalday(lowest_start_time).capitalize()}-{datetime.datetime.strftime(lowest_start_time, "%H:%M")}-{lowest_title}')

if __name__ == "__main__":
    getnextevent()
