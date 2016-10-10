'''Author: Wynand
Started: 20141125
Last updated: 20141129'''

# Python standard library
import datetime as dt
import pprint
import sys
import time
from collections import namedtuple
# Third party modules
import httplib2
import lxml.html
import oauth2client.client
import requests
from apiclient import discovery
from apiclient import errors
from apiclient import http
from apiclient.http import MediaFileUpload
from bs4 import BeautifulSoup
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

download_url = 'http://pastebin.com/u/reborn4HD-nfl'
# The URL where the nfl games live

rd = requests.get(download_url)
soup_rd = BeautifulSoup(rd.content)
raw_links_dl = soup_rd.findAll("a")

dl = {}
# dl will be our dictionary of link:description

for link in raw_links_dl:
    if "NFL" in link.text:
        dl[link.get("href")] = link.text

# We now have a reference dictionary of all of the pastbin links and their titles
# We now want to find the latest week

def search_dl(dl, lookup):
    for k, v in dl.items():
        if lookup in v:
         return k

# We can now return a pastebin address based on a date

# Next we need to find the date of the last and next 49ers games

sf_url = "http://www.reddit.com/r/49ers/"
rsf = requests.get(sf_url)
soup_rsf = BeautifulSoup(rsf.content)
raw_links_sf = soup_rsf.findAll("td")

Game = namedtuple('Game', 'date time where opponent result')
# This creates out named tuple with all of the headings inside it

schedule = soup_rsf.select("div.md tbody")[1]
""" From inspecting element the table with the fixtures is under "div class = 'md'", the table contents is
defined by 'tbody', and it is the second table, thus the [1]"""

# Sometime we get an 'IndexError: list index out of range'. Can try to fix this by just rerunning code until it works

season = []
# The blank dictionary to which each "Game" named tuple will be added

for row in schedule.findAll("tr"):
    fixture = Game._make([td.text for td in row.findAll("td")])
    season.append(fixture)

# We now have a namedtuple that has every game from the subreddit sidebar in it
# Now we need to find the latest game played

#to look up values in tuple can use:
#for fixture in season:
#  ....:     print (fixture.date, fixture.opponent, fixture.result)


today = dt.date.today()
yesterday = today - dt.timedelta(days = 1)
today_pastebin_formatted = today.strftime("%Y.%m.%d")
today_sfsidebar_formatted = today.strftime("%m/%d")
yesterday_pastebin_formatted =yesterday.strftime("%Y.%m.%d")
yesterday_sfsidebar_formatted = yesterday.strftime("%m/%d")

games_today_yesterday = []

for fixture in season:
    if fixture.date == today_sfsidebar_formatted:
        games_today_yesterday.append(fixture.date)
    elif fixture.date == yesterday_sfsidebar_formatted:
        games_today_yesterday.append(fixture.date)

# We now have a tuple that has a value in it if there is a game today or yesterday
# Currently the times are based on AMERICAN, so need to offset by 24hrs
# To offset simply add a third day option of 'twodaysago'

twodaysago = today - dt.timedelta(days = 2)
twodaysago_pastebin_formatted = twodaysago.strftime("%Y.%m.%d")
twodaysago_sfsidebar_formatted = twodaysago.strftime("%m/%d")

for fixture in season:
    if fixture.date == twodaysago_sfsidebar_formatted:
        games_today_yesterday.append(fixture.date)


# Our tuple now includes the game if it was twodaysago in USA terms, which is ~24hrs after the game in Aus
# We now need to take the date in games_today_yesterday and find it in the dl dictionary

year = "/2014"
game_wanted = games_today_yesterday[0]
game_wanted = game_wanted + year

# We now have our game wanted date in the form %mm/%dd/%yyyy

game_wanted = time.strptime(game_wanted, "%m/%d/%Y")
game_wanted = time.mktime(game_wanted)
game_wanted = dt.datetime.fromtimestamp(game_wanted)
game_wanted = game_wanted.strftime("%Y.%m.%d")

# We now have a dt value in the form %yyy.%mm.%dd for the game played in the previous 48 hours

pastebin_download_url = search_dl(dl,game_wanted)
pastebin_download_url = "http://pastebin.com{0}".format(pastebin_download_url)

if pastebin_download_url == "http://pastebin.comNone":
    sys.exit(0)

# We now have the pastebin link where we should be looking for the SF game

# Next we need to go to that url and find the download URLs to copy into jdownloader

rpdl = requests.get(pastebin_download_url)
soup_rpdl = BeautifulSoup(rpdl.content)
raw_links_pastebin = soup_rpdl.findAll("li")

download_links = []

for row in raw_links_pastebin:
    if all(["49ers" in row.text, "540p" in row.text, "720p" not in row.text]):
        download_links.append(row.text)

# We now have a tuple with the 5 download links (1 for full game + 4 quarters) in it
# Next we need to add these links to a text file, and upload it to google drive

f = open('/home/wynand/Desktop/Python Programs/Sport Downloader/Download Links.txt',"w")
for t in download_links:
    f.write("\ntext={0}\nautoStart=TRUE\n".format(t))
f.close()

# We now have a .txt file that we can convert to a .crawljob

# Next we have to upload it to google drive
# The next lines of code come from "https://developers.google.com/drive/web/examples/python"

flow = flow_from_clientsecrets('/home/wynand/Desktop/Python Programs/Sport Downloader/client_secrets.json',
                               scope='https://www.googleapis.com/auth/drive',
                               redirect_uri='urn:ietf:wg:oauth:2.0:oob')

#retrieve if available
storage = Storage('/home/wynand/Desktop/Python Programs/Sport Downloader/OAuthcredentials.txt')
credentials = storage.get()

if  credentials is None:
    #step 1
    auth_uri = flow.step1_get_authorize_url() # Redirect the user to auth_uri
    print ('Go to the following link in your browser: ' + auth_uri)
    code = input('Enter verification code: ').strip()
    #step 2
    credentials = flow.step2_exchange(code)
else:
    print ('GDrive credentials are still current')

#authorise
http = httplib2.Http()
http = credentials.authorize(http)
print ('Authorisation successfully completed')

#build
drive = discovery.build('drive', 'v2', http=http)

#store for next time
storage.put(credentials)

# We are now authorised to upload to drive, now need to do the actual uploading

# Path to the file to upload.
file_name = '/home/wynand/Desktop/Python Programs/Sport Downloader/Download Links.txt'

# Metadata about the file.
file_title = 'Download Links.txt'
file_description = 'A shiny new text file containing the download links for the games i care about.'
parent_id = [{'id': "0BzOWafUuF9rvUkx6MTR6NjE5bFE"}]
# Parent id is the folder location, can be found as the last code in the browser window

# Insert a file. Files are comprised of contents and metadata.
# MediaFileUpload abstracts uploading file contents from a file on disk.
media_body = MediaFileUpload(file_name, mimetype="", resumable=True)

# The body contains the metadata for the file.
body = {'title': file_title, 'description': file_description, 'parents':parent_id}

# Perform the request and print the result.
file_upload = drive.files().insert(body=body, media_body=media_body).execute()
pprint.pprint(file_upload)

# https://stackoverflow.com/questions/16810266/need-to-get-oauth-flow-flowing-for-google-drive-on-python-for-a-stand-alone-py
# https://github.com/googledrive/python-quickstart/blob/master/main.py

"""Next I need to make it autoloop when it hits the out of range error
and update files instead of uploading multiple (https://developers.google.com/drive/v2/reference/files/update)"""
