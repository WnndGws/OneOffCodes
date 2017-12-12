#!/bin/python
'''Takes a image from wallpaper_dir and adds a random quote from quote_file
then sets this as the wallpaper

TODO:
* create a click.option, that when used doesnt need a wallpaper directory,
  instead uses the daily bing wallpaper
* cleanup option names
* cleanup errors that occur when forget to run "change_wallpaper" or "download_bing_wallpaper"
* add option to set bing wallpaper dir (defaulting to tmp/)
'''

import json
import os
import random
from subprocess import call
import textwrap
import socket

import click
from PIL import Image, ImageDraw, ImageFont
import requests


# create a click group to download bing wallpaper
@click.group()
def run_download_bing_wallpaper():
    '''downloads Bing daily wallpaper'''
    pass

# create click command to download daily bing wallpaper
@run_download_bing_wallpaper.command(
    context_settings=dict(ignore_unknown_options=True,
                          allow_extra_args=True,
                          resilient_parsing=True)
)
@click.option(
    '--country',
    prompt=True,
    type=click.Choice(['en-US', 'zn-CN', 'ja-JP', 'en-AU', 'en-UK', 'de-DE', 'en-NZ', 'en-CA']),
    default='en-AU',
    help="Choose the country location of the Bing wallpaper you want to use [DEFAULT: en-AU]"
    )
@click.option(
    '--resolution',
    type=click.Choice(['1920x1200', '1920x1080', '1366x768', '1280x720', '1024x768']),
    default='1920x1080',
    prompt=True,
    help="Choose the resolution of the image you want to download [DEFAULT: 1920x1080]"
)

def download_bing_wallpaper(country, resolution):
    '''Downloads the daily wallpaper from bing as a jpg'''
    # idx determines where to start from. 0 is today, 1 is yesterday, etc.
    idx = "0"
    mkt = country
    resolution = resolution
    url = f'https://www.bing.com/HPImageArchive.aspx?format=js&idx={idx}&n=1&mkt={mkt}'

    r = requests.get(url)
    if r.status_code == 200:
        json_dict = json.loads(r.content)['images'][0]
        image_url = json_dict['urlbase']
        image_url = f'https://www.bing.com/{image_url}_{resolution}.jpg'
        r = requests.get(image_url)
        if r.status_code == 200:
            with open('/tmp/bing.jpg', 'wb') as f:
                f.write(r.content)

# create click command to add quote to image and set that as wallpaper
@click.group()
def run_change_wallpaper():
    '''click group to run the change_wallpaper function'''
    pass

@run_change_wallpaper.command(
    context_settings=dict(ignore_unknown_options=True,
                          allow_extra_args=True,
                          resilient_parsing=True)
)
@click.pass_context
@click.option(
    '--wallpaper-dir',
    type=click.Path(),
    default='~/Pictures',
    help="Path to the wallpaper directory [DEFAULT: ~/Pictures]"
)

@click.option(
    '--quote-file',
    type=click.Path(),
    default='~/.config/wallpaperMaker/quotes.txt',
    help="Path to the newline seperated quotes file"
)
@click.option(
    '--font',
    type=click.Path(),
    default='/usr/share/fonts/TTF/Lato-Regular.ttf',
    help="Path to the .ttf font file [DEFAULT: DroidSerif]"
)
@click.option(
    '--font-size',
    default=50,
    help="Font size [DEFAULT: 50]"
)
@click.option(
    '--bing',
    is_flag=True,
    help="Use this flag if you want to use the daily Bing wallpaper instead of a local image"
)
@click.pass_context
@click.argument('leftover_args', nargs=-1, type=click.UNPROCESSED)

def change_wallpaper(self, ctx, wallpaper_dir, quote_file, font, font_size, bing, leftover_args):
    '''Add quote selected from text file over images in a folder'''

    # set font
    quote_font = ImageFont.truetype(font, font_size)
    # get an image
    if bing:
        ctx.invoke(download_bing_wallpaper)
        base_image = Image.open('/tmp/bing.jpg').convert('RGBA')
        #call(["wal", "-c", "-i", "/tmp/bing.jpg"])
    else:
        random_wallpaper = random.choice(os.listdir(wallpaper_dir))
        base_image = Image.open(wallpaper_dir + "/" + random_wallpaper).convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    text_image = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
    with open(quote_file) as f:
        quote_pool = f.read().splitlines()
    random_quote = random.choice(quote_pool)
    quote_lines = textwrap.wrap(random_quote, width=60)

    # get a drawing context
    draw = ImageDraw.Draw(text_image)
    # determine location of text
    x_loc = base_image.size[0]
    # determine the size of one line of the quote, and multiply by how many lines giving the y-size
    quote_size_y = len(quote_lines)*quote_font.getsize(quote_lines[0])[1]
    # determine x size by seeing how wide the text will be
    quote_size_x = quote_font.getsize(quote_lines[0])[0]
    # put the quote so the centre always matches the centre of the image
    y_loc = base_image.size[1]/2 - (quote_size_y/2)

    # draw text
    for line in quote_lines:
        line_width, line_height = quote_font.getsize(line)
        draw.text(((x_loc - line_width - 20), y_loc),
                  line, font=quote_font,
                  fill=((255, 255, 255, 128)))
        y_loc += line_height

    textbox_image = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(textbox_image)
    x_loc = base_image.size[0]
    y_loc = base_image.size[1]/2 - (quote_size_y/2)
    draw.rectangle(((x_loc - quote_size_x * 1.15), y_loc - 10,
                    x_loc - 10, y_loc + quote_size_y + 10),
                   (0, 0, 0, 128))

    image_out = Image.alpha_composite(base_image, textbox_image)
    image_out = Image.alpha_composite(image_out, text_image)

    image_out.save("/tmp/wallpaper.png")
    call(["feh", "--bg-scale", "/tmp/wallpaper.png"])

RUN_WALLPAPER = click.CommandCollection(sources=[run_download_bing_wallpaper, run_change_wallpaper])

def is_connected():
    remote_server = "www.google.com"
    try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
        host = socket.gethostbyname(remote_server)
    # connect to the host -- tells us if the host is actually
    # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False

if __name__ == "__main__" and is_connected() is True:
    RUN_WALLPAPER()
