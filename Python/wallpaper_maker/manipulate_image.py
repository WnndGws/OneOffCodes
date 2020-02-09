#!/bin/python3
"""Adds quote box to image
"""

import download_wallpaper_image
import click

@click.command()
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
    help="Path to the newline separated quotes file",
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
    help="Use this flag if you want to use the daily Bing wallpaper instead of a local im
    )
@click.option(
    "--agenda",
    is_flag=True,
    help="Use if want to append your day's agenda to the quote",
    )
def mannipulate_wallpaper(wallpaper_dir, quote_file, font, font_size, bing, agenda):
    #set font
    quote_font = ImageFont.truetype(font, font_size)

    #get image
