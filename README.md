# Tagesschau Corona Counter

A simple web-scraper that provides utilities to count the number of occurences of "Corona" and related keywords within the recent 30 days in the "20 Uhr Tagesschau" topic list.

## Setup
  1. Requires `python3`
  1. Install dependencies `pip3 install -r requirements.txt`

## HTTP Service
  The HTTP service consits of two paths. First, `/find/<term>` which searches for hits for a `term` and `/text` which returns the text for a given range of dates.

  To run the service simply run `2-http.py`.

  Now you can send requests such as `find/Corona?start=2021.01.15&end=2020.01.20` which will return a JSON object with a property `result` containing an array of size 6 (15th to 20th January) containing a boolean for each date. The boolean indicates whether the string `Corona` was contained in the topics description for that date.

  To get the texts for range of dates date simply make a call such as `/text?start=2021.01.15&end=2021.01.20` which will return a JSON with a `result` property containing an element of text for each date from `2021.01.15` to `2021.01.20`.

  To get the aggregations for a range of dates you can use `/sum/<term>?n=<n>&start=<date>&end=<date>`. For each `date` in the range between `start` and `end` (including both), it will count the number of days among the most-recent `N` days where `term` was contained in that day's text. The response is a JSON with a `result` property being an array with an element for each day in the date-range. For example, if `Corona` occurred in the text on Monday, Tuesday, Thursday and Saturday, then the result for `n = 4` will be `2`. This is because only Tuesday and Thursday in [Tuesday, Wednesday, Thursday, Friday] are counted. Note, that `N >= 1` and that the contributions from days before `start` are needed to count the sum for the first `N-1` elements of the result.

## Downloading the data
  You can web-scrape and download all topic descriptions for  specified a time period.

  1. Edit `config.yml` and set `start-date` and `end-date` to the first and last dates for which you want to download the text. Please use the format specified in `date-format`.
  1. Run `python3 1-download-data.py`
  1. Run `./summarize-topic-lengths.sh` (Linux only) to see how many characters each day's topic description has. If some description is suspiciously small or large, perhaps something was scraped and mistaken as the topic description.
  1. View the topic descriptions in the respective files in `data` - i.e. `data/topics-2021.01.15.txt` for `2021.15.01`

## Dataset
  It was verified that the download of the topics text succeeds for all dates from `2014.01.01` to `2021.01.22`. Expected failure dates are recorded in `config.yml` in `ignore-error-dates`. For these dates, en empty text is added automatically.
