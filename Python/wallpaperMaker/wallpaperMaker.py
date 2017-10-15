#!/bin/python
'''Takes a image from WALLPAPER_DIR and adds a random quote from QUOTE_FILE
then sets this as the wallpaper'''

import textwrap
import os
import sys
import random
from subprocess import call

from PIL import Image, ImageDraw, ImageFont

WALLPAPER_DIR = '/home/wynand/GoogleDrive/01_Personal/01_Personal/05_Images/Wallpapers'
QUOTE_FILE = sys.path[0] + '/quotes.txt'

# get a font
FNT = ImageFont.truetype('/usr/share/fonts/TTF/DroidSerif-Regular.ttf', 50)

def change_wallpaper():
    '''Add quote selected from text file over images in a folder'''

    # get an image
    random_wallpaper = random.choice(os.listdir(WALLPAPER_DIR))
    base_image = Image.open(WALLPAPER_DIR + "/" + random_wallpaper).convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    text_image = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
    with open(QUOTE_FILE) as f:
        quote_pool = f.read().splitlines()
    random_quote = random.choice(quote_pool)
    quote_lines = textwrap.wrap(random_quote, width=60)

    # get a drawing context
    draw = ImageDraw.Draw(text_image)
    # determine location of text
    x_loc = base_image.size[0]
    # determine the size of one line of the quote, and multiply by how many lines giving the y-size
    quote_size_y = len(quote_lines)*FNT.getsize(quote_lines[0])[1]
    # determine x size by seeing how wide the text will be
    quote_size_x = FNT.getsize(quote_lines[0])[0]
    # put the quote so the centre always matches the centre of the image
    y_loc = base_image.size[1]/2 - (quote_size_y/2)

    # draw text
    for line in quote_lines:
        line_width, line_height = FNT.getsize(line)
        draw.text(((x_loc - line_width - 20), y_loc), line, font=FNT, fill=((255, 255, 255, 128)))
        y_loc += line_height

    textbox_image = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(textbox_image)
    x_loc = base_image.size[0]
    y_loc = base_image.size[1]/2 - (quote_size_y/2)
    draw.rectangle(((x_loc - quote_size_x * 1.05), y_loc - 10, x_loc - 10, y_loc + quote_size_y + 10), (0, 0, 0, 128))

    image_out = Image.alpha_composite(base_image, textbox_image)
    image_out = Image.alpha_composite(image_out, text_image)

    image_out.save("/tmp/wallpaper.png")
    call(["feh", "--bg-scale", "/tmp/wallpaper.png"])

if __name__ == "__main__":
    change_wallpaper()
