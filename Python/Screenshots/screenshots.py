#!/usr/bin/python3
## So I can take screenshots and share them

import datetime
import os
import re
import requests
import subprocess
import time

## Set file name and path
user_home = os.path.expanduser("~/")
save_dir = "GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots/"
file_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%T")

## Call scrot from command line since this is easier and more robust
# than doing it in python
print ("Select area to share.....")
subprocess.call(["scrot", f"{user_home}{save_dir}{file_name}.png", "-q 100", "-s"])

## Find most recent file (ie. just created file) in savedir
file_to_share = os.listdir(f'{user_home}{save_dir}')
file_to_share.sort()
file_to_share = file_to_share[-1]

## Upload to GoogleDrive using Insync-headless
sync_progress = subprocess.Popen(["insync-headless", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

## Since insync has a delay, need to wait for status change first, and
# only then can check if done uploading
print ("Uploading.....\033[0K\r")
while sync_progress.stdout.readline() != "Uploading\n":
    time.sleep(1)
    sync_progress = subprocess.Popen(["insync-headless", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

while sync_progress.stdout.readline() != "No syncing activities\n":
    time.sleep(1)
    sync_progress = subprocess.Popen(["insync-headless", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

subprocess.Popen(["xsel", "-cp"])
subprocess.Popen(["xsel", "-cc"])

## Copy the actual image to the clipboard buffer
print ("Copying image to clipboard.....")
subprocess.run(["xclip", "-selection", "clipboard|primary|secondary", "-t", "image/png", "-i", f"{user_home}{save_dir}{file_to_share}"])
subprocess.run(["feh", f"{user_home}{save_dir}{file_to_share}"])

## Use Insync to get public link of file and copy it to primary buffer
print ("Getting public link.....")
copy_to_primary = subprocess.Popen(["xsel", "-pi"], stdin=subprocess.PIPE)
public_url = b'\n'
while public_url.decode() == "\n":
    time.sleep(5)
    public_url = subprocess.check_output(["insync-headless", "get_public_link", f'{user_home}{save_dir}{file_to_share}'])
image_id = re.findall(r'[^\/]{33}', public_url.decode())
public_url = requests.get(f"https://drive.google.com/uc?id={image_id[0]}&export=image", allow_redirects=True)
copy_to_primary.communicate(public_url.url.encode())

## Delete any file in save_dir older than 7d
time_now = float(datetime.datetime.now().strftime("%s"))
for file in os.listdir(f'{user_home}{save_dir}'):
    time_creation = os.path.getctime(f'{user_home}{save_dir}{file}')
    if (time_now - time_creation) // (24*3600) >= 7:
        print (f'Removing {file}')
        os.remove(f'{user_home}{save_dir}{file}')
