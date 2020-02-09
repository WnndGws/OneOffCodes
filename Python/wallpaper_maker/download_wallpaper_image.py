#!/bin/python3
"""Downloads that days bing background image
"""

import json
import requests
import click

@click.command()
@click.option(
    "--country",
    prompt=True,
    type=click.Choice(
        ["en-US", "zn-CN", "ja-JP", "en-AU", "en-UK", "de-DE", "en-NZ", "en-CA"]
    ),
    default="en-AU",
    help="Choose the country location of the Bing wallpaper you want to use [DEFAULT: en-AU]",
)
@click.option(
    "--resolution",
    type=click.Choice(["1920x1200", "1920x1080", "1366x768", "1280x720", "1024x768"]),
    default="1920x1080",
    prompt=True,
    help="Choose the resolution of the image you want to download [DEFAULT: 1920x1080]",
)
def download_bing_wallpaper(country, resolution):
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
