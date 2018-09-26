#!/usr/bin/python3
## A python script to add events to my calendar to remind me to watch sport that happened overnight

## TODO: Handle events without description/location etc

import calendar
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime
from dateutil.parser import parse
import click

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    # If modifying these scopes, delete your previously saved credentials
    SCOPES = "https://www.googleapis.com/auth/calendar"
    CLIENT_SECRET_FILE = "calendar_reminder_client_secrets.json"
    APPLICATION_NAME = "Sport_Reminder"
    flags = None

    home_dir = os.path.expanduser("~")
    credential_dir = os.path.join(home_dir, ".config/credentials")
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, "calendar_reminder_saved_credentials.json")
    CLIENT_SECRET_FILE = os.path.join(credential_dir, CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)
    return credentials

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
@click.option("--add-to-calendar", is_flag=True, help="Add results to your calendar")
@click.option("--source-calendar-url", help="The URL to the calendar to check. In the form 'aaaaaaaaaaaaa@group.calendar.google.com'", prompt=True)
def main(start, months, verbose, add_to_calendar, source_calendar_url):
    """Scrapes source calendar and adds reminders to calendar to watch sport that occured overnight"""

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)

    end = add_months(datetime.datetime.strptime(start, "%Y-%m-%d"), months)
    start = start + "T00:00:00Z"
    end = end.isoformat() + "T00:00:00Z"

    eventsResult = (
        service.events()
        .list(
            calendarId=source_calendar_url,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = eventsResult.get("items", [])

    if verbose:
        for event in events:
            eventTitle = event["summary"]
            click.echo(f'{eventTitle}')

    if add_to_calendar:
        for event in events:
            reminderEvent = {}
            for item in ["summary", "location", "description", "start", "end"]:
                reminderEvent[item] = event[item]

            reminderEvent["summary"] = f'REMINDER: {event["summary"]}'
            reminderEvent["start"] = {"dateTime": f'{datetime.datetime.strftime(parse(event["end"]["dateTime"]) + datetime.timedelta(days=0), "%Y-%m-%dT19:00:00%z")}'}
            reminderEvent["end"] = {"dateTime": f'{datetime.datetime.strftime(parse(event["end"]["dateTime"]) + datetime.timedelta(days=0), "%Y-%m-%dT20:00:00%z")}'}
            service.events().insert(
                calendarId="ucuu438np9dss601ueh11d2vp4@group.calendar.google.com",
                body=reminderEvent).execute()
            click.echo(f"Adding {reminderEvent['summary']} to calendar......")

if __name__ == "__main__":
    main()
