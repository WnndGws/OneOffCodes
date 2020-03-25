#!/bin/python3
"""Downloads that days bing background image
"""

import json
import requests

def download_bing_wallpaper():

    country = "en-AU"
    resolution = "1920x1080"

    """Downloads the daily wallpaper from bing as a jpg"""
    # idx determines where to start from. 0 is today, 1 is yesterday, etc.
    idx = "0"
    mkt = country
    resolution = resolution
    url = f"https://www.bing.com/HPImageArchive.aspx?format=js&idx={idx}&n=1&mkt={mkt}"

    r = requests.get(url)
    if r.status_code == 200:
        json_dict = json.loads(r.content)["images"][0]
        image_url = json_dict["urlbase"]
        image_url = f"https://www.bing.com/{image_url}_{resolution}.jpg"
        r = requests.get(image_url)
        if r.status_code == 200:
            with open("/tmp/bing.jpg", "wb") as f:
                f.write(r.content)

if __name__ == "__main__":
    download_bing_wallpaper()
