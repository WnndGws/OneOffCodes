#!/usr/bin/python3
## Written to replace the next_event.sh. Checks google calendar for next event and displays it nicely

import os
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import click
import datetime
from apiclient import discovery
import httplib2
import humanize
from pytz import timezone
import re

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "nextevent2clientsecrets.json"
    APPLICATION_NAME = "Next Event 2.0"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
       os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "nextevent2savedcredentials.json")
    CLIENT_SECRET_FILE = os.path.join(credential_dir, CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
       flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
       flow.user_agent = APPLICATION_NAME
       credentials = tools.run_flow(flow, store, flags)
       print("Storing credentials to " + credential_path)
    return credentials

def getnextevent():
    """ Loops through all calendars and prints the next even in each one """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    # 'Z' needed for calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.date.today().isoformat()
    today = datetime.datetime.strptime(today, "%Y-%m-%d")

    location = 'Australia/Perth'
    tz = timezone(location)
    # Need to change times to non-naive
    event_title_low = None
    page_token = None

    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    # Get next event in each calendar
    timed_events =[]
    allday_events = []
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
        if event != []:
            #Determine start time
            try:
                event_time = {event[0]["start"]["dateTime"]}
                for start_time in event_time:
                    if start_time[-1] == 'Z':
                        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
                        start_time = start_time + datetime.timedelta(hours = 8)
                        start_time = tz.localize(start_time)
                    else:
                        start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
                #calendar_entry = [start_time, end_time, event[0]["summary"]]
                #timed_events.append(calendar_entry)
            except:
                event_time = {event[0]["start"]["date"]}
                for start_time in event_time:
                    start_time = start_time
                #calendar_entry = [start_time, end_time, event[0]["summary"]]
                #allday_events.append(calendar_entry)

            #Determine end time
            try:
                event_time = {event[0]["end"]["dateTime"]}
                for end_time in event_time:
                    if end_time[-1] == 'Z':
                        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")
                        end_time = end_time + datetime.timedelta(hours = 8)
                        end_time = tz.localize(end_time)
                    else:
                        end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
                duration = end_time - start_time
                duration = duration.seconds
                calendar_entry = [start_time, end_time, event[0]["summary"], duration]
                timed_events.append(calendar_entry)
            except:
                event_time = {event[0]["end"]["date"]}
                for end_time in event_time:
                    end_time = end_time
                calendar_entry = [start_time, end_time, event[0]["summary"]]
                allday_events.append(calendar_entry)

    event_start_low = allday_events[0][0]
    for i in allday_events:
        #print(f'{i[0]} - {i[1]}: {i[2]}')
        if i[0] <= event_start_low:
            event_start_low = i[0]
            lowest_allday = [i[0],i[1], i[2]]
    event_start_low = timed_events[0][0]
    for i in timed_events:
        #Only want events shorter than 11hrs
        #print(f'{i[0]} - {i[1]}: {i[2]}')
        if i[0] <= event_start_low and 1 < i[3] < 39601:
            event_start_low = i[0]
            lowest_timed = [i[0], i[1], i[2], i[3]]

    #Determine which is lower
    #If event occurs less than 24hrs after allday event starts its in the same day
    if (lowest_timed[0] - tz.localize(datetime.datetime.strptime(lowest_allday[0], "%Y-%m-%d"))).seconds < 86400:
        start_time_print = humanize.naturalday(lowest_timed[0]).title() + "-" + datetime.datetime.strftime(lowest_timed[0], "%H:%M")
        #start_time_print = datetime.datetime.strftime(lowest_timed[0], "%H:%M")
        print(f'{start_time_print}-{lowest_timed[2]}')
        #print(lowest_timed)
    elif str(datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d %H:%M:%S")) == str(datetime.datetime.strptime(lowest_allday[0], "%Y-%m-%d")):
        print(f'Today: {lowest_allday[2]}')

if __name__ == "__main__":
    getnextevent()
