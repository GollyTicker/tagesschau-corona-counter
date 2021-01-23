# Tagesschau Corona Counter

A simple web-scraper that provides utilities to count the number of occurences of "Corona" and related keywords within the recent 30 days in the "20 Uhr Tagesschau" topic list.

## Setup
  1. Requires `python3`
  1. Install dependencies `pip3 install -r requirements.txt`

## Usage
  You can web-scrape and download all topic descriptions for  specified a time period.

  1. Edit `config.yml` and set `start-date` and `end-date` to the first and last dates for which you want to download the text. Please use the format specified in `date-format`.
  1. Run `python3 1-download-data.py`
  1. Run `./summarize-topic-lengths.sh` (Linux only) to see how many characters each day's topic description has. If some description is suspiciously small or large, perhaps something was scraped and mistaken as the topic description.
  1. View the topic descriptions in the respective files in `data` - i.e. `data/topics-2021.01.15.txt` for `2021.15.01`

## Dataset
It was verified that the download of the topics text succeedes for all dates from `2014.01.01` to `2021.01.22`. Expected failure dates are recorded in `config.yml` in `ignore-error-dates`. For these dates, en empty text is added automatically.
