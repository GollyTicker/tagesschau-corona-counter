# Tagesschau Corona Counter

A simple web-scraper that provides utilities to count the number of occurences of "Corona" and related keywords within the recent 30 days in the "20 Uhr Tagesschau" topic list.

## Setup
  1. Requires `python3`
  1. Install dependencies `pip3 install -r requirements.txt`

## HTTP Service
  The HTTP service consits of two paths. First, `/find/<term>` which searches for hits for a `term` and `/file/<date>` which returns the text for a given date.

  To run the service simply run `2-http.py`.

  Now you can send requests such as `find/Corona?start=2021.01.15&end=2020.01.20` which will return a JSON object with a property `result` containing an array of size 6 (15th to 20th January) containing a boolean for each date. The boolean indicates whether the string `Corona` was contained in the topics description for that date.

  To get the text for a given date simply make a call such as `/file/2021.01.15` which will return a JSON with a `result` property containing the text as a string.

## Downloading the data
  You can web-scrape and download all topic descriptions for  specified a time period.

  1. Edit `config.yml` and set `start-date` and `end-date` to the first and last dates for which you want to download the text. Please use the format specified in `date-format`.
  1. Run `python3 1-download-data.py`
  1. Run `./summarize-topic-lengths.sh` (Linux only) to see how many characters each day's topic description has. If some description is suspiciously small or large, perhaps something was scraped and mistaken as the topic description.
  1. View the topic descriptions in the respective files in `data` - i.e. `data/topics-2021.01.15.txt` for `2021.15.01`

## Dataset
  It was verified that the download of the topics text succeeds for all dates from `2014.01.01` to `2021.01.22`. Expected failure dates are recorded in `config.yml` in `ignore-error-dates`. For these dates, en empty text is added automatically.
