#!/usr/bin/python3
##Outputs my daily events from google calendar

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

#try:
    #import argparse
    #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
    #flags = None
flags = None

SCOPES = "https://www.googleapis.com/auth/calendar.readonly"
home_dir = os.path.expanduser("~")
CLIENT_SECRET_FILE = os.path.join(
    home_dir, ".config/saved_credentials/wallpaper_client_secrets.json"
)
APPLICATION_NAME = "Wallpaper_maker"


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/saved_credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "wallpaper_maker_credentials.json")

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print("Storing credentials to " + credential_path)
    return credentials

def get_events():
    """
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    now = datetime.date.today().isoformat()
    now = now + "T00:00:00Z"
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    tomorrow = tomorrow + "T00:00:00Z"
    tomorrowPlusOne = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
    tomorrowPlusOne = tomorrowPlusOne + "T00:00:00Z"

    allEvents = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            eventResult = (
               service.events()
               .list(
                   calendarId=calendar_list_entry["id"],
                   timeMin=now,
                   timeMax=tomorrowPlusOne,
                   singleEvents=True,
                   orderBy="startTime",
               )
               .execute()
            )
            events = eventResult.get("items", [])
            if not events:
                pass
            for event in events:
                allEvents.append(event)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


    return allEvents

def main():
    """Prints a pretty list of events
    """

    allEvents = get_events()
    today = datetime.date.today().strftime("%Y/%m/%d")
    textListToday = []
    textListTodayAllDay = []
    textListTomorrow = []
    textListTomorrowAllDay = []
    textBox = ""

    for event in allEvents:
        try:
            start = event["start"].get("dateTime")
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S+08:00")
            date = datetime.datetime.strftime(start, "%H:%M")
            start = datetime.datetime.strftime(start, "%Y/%m/%d %H:%M")
            if start[:10] == today:
                textListToday.append(f'{date} {event["summary"]}')
            else:
                textListTomorrow.append(f'{date} {event["summary"]}')
        except:
            start = event["start"].get("date")
            start = datetime.datetime.strptime(start, "%Y-%m-%d")
            start = datetime.datetime.strftime(start, "%Y/%m/%d")
            if start[:10] == today:
                textListTodayAllDay.append(f'{event["summary"]}')
            else:
                textListTomorrowAllDay.append(f'{event["summary"]}')

    textListToday.sort()
    textListTodayAllDay.sort()
    textListTomorrow.sort()
    textListTomorrowAllDay.sort()

    print(textListToday)
    print(textListTomorrow)
    print(textListTodayAllDay)
    print(textListTomorrowAllDay)

if __name__ == "__main__":
    main()
