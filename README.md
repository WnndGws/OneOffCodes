# Scripts

This is a collection of shell scripts, and Python scripts that I write to achieve a discrete task

## Getting Started

All scripts are written for ZSH and/or Python 3.

## Installing
All scripts should be able to run in isolation.
eg.
```
chmod +x script.py
./scripts.py
```

## Descriptions
### Python
* paragraphscraper/article_summarise_cosine
    * [Implementation](https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70) in python to use natural language to summarise an article into the top n most "important" sentences

* paragraphscraper/paragraph_scraper
    * Crawls a url and outputs all "\<p\>" tags to a file

* boxing
    * Checks when [any of the top ranked boxers](https://en.wikipedia.org/wiki/List_of_current_boxing_rankings) are fighting, with optional output to GoogleCalendar

* bspwm_desktopnamer
    * Rename my BSPWM workspaces to include the icons of any open programs on that workspace. Make for a nice polybar

* dustinoffthedegree
    * broken
    * Used to scrape episode numbers and topic from podcast show notes

* ff2mpv
    * Cloned from https://github.com/woodruffw/ff2mpv/
    * Used to open a video in mpv from firefox

* gifmaker
    * Turns a portion of a video into a webm with the help of ffmpeg

* nextevent
    * Outputs the next calendar entry in my GoogleCalendar

* polybar_weather
    * Checks [openweathermap.org](https://openweathermap.org) for the current forcast, and prints it nicely for polybar module

* scienceorfictionscraper
    * Scrapes the SGU for the "science or fiction" section in show notes. Can optionally print answers

### Shell
<++> WIP

## Contributing

I am more than happy to be shown how to improve these scripts. Simply fork, edit, and submit a PR with any changes.

## Authors

* WnndGws

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

