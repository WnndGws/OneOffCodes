#!/bin/python3
"""Adds quote box to image
"""

import download_wallpaper_image
import get_calendar_events

import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageStat

import pdb

def manipulate_wallpaper():

    pdb.set_trace()

    quote_file = "./quotes.txt"
    base_image = Image.open("/tmp/bing.jpg").convert("RGBA")

    #set font
    font = "/usr/share/fonts/TTF/Hack Regular Nerd Font Complete Mono.ttf"
    font_size = 50
    quote_font = ImageFont.truetype(font, font_size)

    #get image
    download_wallpaper_image.download_bing_wallpaper()

    #get agenda
    agenda = get_calendar_events.main()

    # make a blank image for the text, initialized to transparent text color
    text_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    with open(quote_file) as f:
        quote_pool = f.read().splitlines()
    random_quote = random.choice(quote_pool)
    quote_lines = textwrap.wrap(random_quote, width=60)
    quote_lines = quote_lines + "/n" + agenda

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
    square_brightness = int(100 + mean_brightness)

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
            (x_loc - quote_size_x * 1.5),
            y_loc - 10,
            x_loc - 10,
            y_loc + quote_size_y + 10,
        ),
        (0, 0, 0, square_brightness),
    )

    image_out = Image.alpha_composite(base_image, textbox_image)
    image_out = Image.alpha_composite(image_out, text_image)

    image_out.save("/tmp/wallpaper.png")

if __name__ == "__main__":
    manipulate_wallpaper()
