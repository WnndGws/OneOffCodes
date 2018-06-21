#!/bin/python3
"""Takes a image from wallpaper_dir and adds a random quote from quote_file
then sets this as the wallpaper
"""

import click
import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageStat
import random
import re
import requests
import socket
from subprocess import call, check_output
import textwrap
import time


def test_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


# create a click group to download bing wallpaper
@click.group()
def run_download_bing_wallpaper():
    """downloads Bing daily wallpaper"""
    pass


# create click command to download daily bing wallpaper
@run_download_bing_wallpaper.command(
    context_settings=dict(
        ignore_unknown_options=True, allow_extra_args=True, resilient_parsing=True
    )
)
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


# create click command to add quote to image and set that as wallpaper
@click.group()
def run_change_wallpaper():
    """click group to run the change_wallpaper function"""
    pass


@run_change_wallpaper.command(
    context_settings=dict(
        ignore_unknown_options=True, allow_extra_args=True, resilient_parsing=True
    )
)
@click.pass_context
@click.option(
    "--wallpaper_dir",
    type=click.Path(),
    default="~/Pictures",
    help="Path to the wallpaper directory [DEFAULT: ~/Pictures]",
)
@click.option(
    "--quote_file",
    type=click.Path(),
    default="~/.config/wallpaperMaker/quotes.txt",
    help="Path to the newline seperated quotes file",
)
@click.option(
    "--font",
    type=click.Path(),
    default="/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    help="Path to the .ttf font file [DEFAULT: DejaVuSansMono]",
)
@click.option("--font-size", default=50, help="Font size [DEFAULT: 50]")
@click.option(
    "--bing",
    is_flag=True,
    help="Use this flag if you want to use the daily Bing wallpaper instead of a local image",
)
@click.option(
    "--agenda",
    is_flag=True,
    help="Use if want to append your day's agenda to the quote",
)
@click.pass_context
@click.argument("leftover_args", nargs=-1, type=click.UNPROCESSED)
def change_wallpaper(
    self, ctx, wallpaper_dir, quote_file, font, font_size, bing, agenda, leftover_args
):
    """Add quote selected from text file over images in a folder"""

    # set font
    quote_font = ImageFont.truetype(font, font_size)
    # get an image
    if bing:
        if test_internet():
            # Test if bing file exists and check age
            if os.path.isfile("/tmp/bing.jpg"):
                age_of_bing_image = time.time() - os.stat("/tmp/bing.jpg").st_mtime
                if age_of_bing_image > 43200:
                    ctx.invoke(download_bing_wallpaper)
            else:
                ctx.invoke(download_bing_wallpaper)
            base_image = Image.open("/tmp/bing.jpg").convert("RGBA")
        else:
            random_wallpaper = random.choice(os.listdir(wallpaper_dir))
            base_image = Image.open(wallpaper_dir + "/" + random_wallpaper).convert(
                "RGBA"
            )
    else:
        random_wallpaper = random.choice(os.listdir(wallpaper_dir))
        base_image = Image.open(wallpaper_dir + "/" + random_wallpaper).convert("RGBA")

    # make a blank image for the text, initialized to transparent text color
    text_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    with open(quote_file) as f:
        quote_pool = f.read().splitlines()
    random_quote = random.choice(quote_pool)
    quote_lines = textwrap.wrap(random_quote, width=60)
    if agenda:
        if test_internet():
            midday_tomorrow = (
                datetime.date.today() + datetime.timedelta(days=1)
            ).strftime("%Y%m%dT23:59")
            midnight_tomorrow = (
                datetime.date.today() + datetime.timedelta(days=1)
            ).strftime("%Y%m%dT00:01")
            agenda_text = check_output(
                ["gcalcli", "agenda", "--refresh", "2am", "11:59pm"]
            ).decode()
            agenda_text = re.findall(
                r"\d*:[^\\]*", str(agenda_text.encode("ascii", "ignore"))
            )
            agenda_morning = check_output(
                ["gcalcli", "agenda", midnight_tomorrow, midday_tomorrow]
            ).decode()
            agenda_morning = re.findall(
                r"\d*:[^\\]*", str(agenda_morning.encode("ascii", "ignore"))
            )
            # Remove my sleep entries
            for event in agenda_text:
                if event[-5:] == "Sleep":
                    agenda_text.remove(event)
            for event in agenda_morning:
                if event[-5:] == "Sleep":
                    agenda_text.remove(event)

            # Remove duplicate entries
            for duplicate in set(agenda_morning).intersection(agenda_text):
                agenda_morning.remove(duplicate)

            # Pad entries to be the same length
            longest_string_length = max(
                len(max(agenda_text, key=len)), len(max(agenda_morning, key=len))
            ) + 1

            # Zero pad single digit times
            agenda_text_padded = []
            agenda_morning_padded = []
            for event in agenda_text:
                if event[6] == " ":
                    event = "0" + event
                event = event.ljust(longest_string_length, ".")
                agenda_text_padded.append(event)
            for event in agenda_morning:
                if event[6] == " ":
                    event = "0" + event
                event = event.ljust(longest_string_length, ".")
                agenda_morning_padded.append(event)

            # Concatonate into one long string
            if len(agenda_morning_padded) > 0:
                quote_lines = (
                    quote_lines
                    + [" "]
                    + [
                        datetime.date.today()
                        .strftime("%a %d/%m/%Y")
                        .ljust(longest_string_length)
                    ]
                    + agenda_text_padded
                    + [" "]
                    + [
                        (datetime.date.today() + datetime.timedelta(days=1))
                        .strftime("%a %d/%m/%Y")
                        .ljust(longest_string_length)
                    ]
                    + agenda_morning_padded
                )
            elif len(agenda_text_padded) > 0:
                quote_lines = (
                    quote_lines
                    + [" "]
                    + [datetime.date.today().strftime("%a %d/%m/%Y")]
                    + agenda_text_padded
                    + [" "]
                )
            else:
                quote_lines = quote_lines
        else:
            agenda_text = []
            agenda_morning = []

    # get a drawing context
    draw = ImageDraw.Draw(text_image)
    # determine location of text
    x_loc = base_image.size[0]
    # determine the size of one line of the quote, and multiply by how many lines giving the y-size
    quote_size_y = len(quote_lines) * quote_font.getsize(quote_lines[0])[1]
    # determine x size by seeing how wide the text will be
    quote_size_x = quote_font.getsize(quote_lines[0])[0]
    # put the quote so the centre always matches the centre of the image
    y_loc = base_image.size[1] / 2 - (quote_size_y / 2)

    # get average background image brightness by converting to greyscale and getting RMS
    mean_brightness = int(ImageStat.Stat(base_image.convert("L")).mean[0])
    square_brightness = int(255 - mean_brightness)

    # draw text
    for line in quote_lines:
        line_width, line_height = quote_font.getsize(line)
        draw.text(
            ((x_loc - line_width - 20), y_loc),
            line,
            font=quote_font,
            fill=((255, 255, 255, square_brightness)),
        )
        y_loc += line_height

    textbox_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(textbox_image)
    x_loc = base_image.size[0]
    y_loc = base_image.size[1] / 2 - (quote_size_y / 2)
    draw.rectangle(
        (
            (x_loc - quote_size_x * 1.15),
            y_loc - 10,
            x_loc - 10,
            y_loc + quote_size_y + 10,
        ),
        (0, 0, 0, square_brightness),
    )

    image_out = Image.alpha_composite(base_image, textbox_image)
    image_out = Image.alpha_composite(image_out, text_image)

    image_out.save("/tmp/wallpaper.png")
    call(["feh", "--bg-scale", "/tmp/wallpaper.png"])


RUN_WALLPAPER = click.CommandCollection(
    sources=[run_download_bing_wallpaper, run_change_wallpaper]
)

if __name__ == "__main__":
    RUN_WALLPAPER()
