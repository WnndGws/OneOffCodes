#!/usr/bin/python3
## So I can take screenshots and share them

import datetime
import os
import subprocess
import time

user_home = os.path.expanduser("~/")
save_dir = "GoogleDrive/01_Personal/01_Personal/05_Images/Screenshots/"
file_name = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d-%T")

print ("Select area to share.....")
subprocess.call(["scrot", f"{user_home}{save_dir}{file_name}.png", "-q 100", "-s"])

file_to_share = os.listdir(f'{user_home}{save_dir}')
file_to_share.sort()
file_to_share = file_to_share[-1]

sync_progress = subprocess.Popen(["insync", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

while sync_progress.stdout.readline() != "Uploading\n":
    print ("Uploading.....")
    time.sleep(1)
    sync_progress = subprocess.Popen(["insync", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

while sync_progress.stdout.readline() != "No syncing activities\n":
    print ("Uploading.....")
    time.sleep(1)
    sync_progress = subprocess.Popen(["insync", "get_sync_progress"], stdout=subprocess.PIPE, universal_newlines=True)

subprocess.Popen(["xsel", "-cp"])
copy_to_primary = subprocess.Popen(["xsel", "-pi"], stdin=subprocess.PIPE)
public_url = subprocess.check_output(["insync", "get_public_link", f'{user_home}{save_dir}{file_to_share}'])
while public_url.decode() == "\n":
    time.sleep(1)
    public_url = subprocess.check_output(["insync", "get_public_link", f'{user_home}{save_dir}{file_to_share}'])
copy_to_primary.communicate(public_url)
