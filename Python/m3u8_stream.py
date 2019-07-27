#!/usr/bin/python3
''' Streams a m3u8 stream to Chromecast
'''

import click
import time
import pychromecast

@click.command()
@click.option(
    "--url",
    prompt=True,
    help="The URL of the website to check"
    )
def cast_now(url):
    chromecasts = pychromecast.get_chromecasts()
    cast = next(cc for cc in chromecasts if cc.device.friendly_name == "Lisa's RuV TV")
    cast.wait()

    mc = cast.media_controller
    mc.play_media(f"{url}", "video/mp4")
    mc.block_until_active()
    print(mc.status)

if __name__ == "__main__":
    cast_now()
