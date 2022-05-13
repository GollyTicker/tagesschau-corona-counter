# Tagesschau Corona Counter

A simple web-scraper that provides utilities to count the number of occurences of "Corona" and related keywords within
the recent 30 days in the "20 Uhr Tagesschau" topic list.

## Setup

1. Requires `docker` and `docker-compose`
1. Requires [local-persist](https://github.com/MatchbookLab/local-persist#installing--running) plugin.
1. Follow the [download instructions](#downloading-the-data) below

## Starting the service

```./restart-service.sh```

Given the configuration `config/config.yml`, it starts

* `tagesschau-api`, the HTTP data service at the port `api-port`
* `tagesschau-web`, the web server running at port `web-port`
* `tagesschau-reloader`, a service which downloads new data once per day and ensures new data is used in the other
  services

In addition to the HTTP data service it starts another container that downloads the latest data from Tagesschau once per
day.

## HTTP Data Service

The HTTP data service `tagesschau-api` consists of three paths.

* `/find/<term>` which searches for hits for a `term`
* `/text` which returns the text for a given range of dates and
* `/sum/<term>` which counts the occurances of a term in the most-recent days for a given range

To run the service simply run `./restart-http-service.sh` (or invoke `src/2-http.py` if outside docker).

Now you can send requests such as `find/Corona?start=2021.01.15&end=2020.01.20` which will return a JSON object with a
property `result` containing an array of size 6 (15th to 20th January) containing a boolean for each date. The boolean
indicates whether the string `Corona` was contained in the topics description for that date.

To get the texts for range of dates date simply make a call such as `/text?start=2021.01.15&end=2021.01.20` which will
return a JSON with a `result` property containing an element of text for each date from `2021.01.15` to `2021.01.20`.

To get the aggregations for a range of dates you can use `/sum/<term>?n=<n>&start=<date>&end=<date>`. For each `date` in
the range between `start` and `end` (including both), it will count the number of days among the most-recent `N` days
where `term` was contained in that day's text. The response is a JSON with a `result` property being an array with an
element for each day in the date-range. For example, if `Corona` occurred in the text on Monday, Tuesday, Thursday and
Saturday, then for day Friday and `n = 4` the result will be `2`. This is because only Tuesday and Thursday
in `[Tuesday, Wednesday, Thursday, Friday]` contribute to the count. Note, that `N >= 1` and that the contributions from
days before `start` are needed to count the sum for the first `N-1` elements of the result.

If you download new data, you will need to restart the HTTP-Server as it loads everything into memory during startup for
higher performance during requests. For that simply use `docker restart tagesschau-api`.

The automatic scheduled update of the data also restarts the http service container `tagesschau-api` to refresh its
cache.

## Downloading the data

You can web-scrape and download all topic descriptions for specified a time period.

1. Edit `config/config.yml` and set `start-date` and `end-date` to the first and last dates for which you want to download the
   text. Please use the format specified in `date-format`. Alternatively, you can set `end-date` to `latest` which will
   download until the last aired show.
1. Run `python3 src/1-download-data.py` (only outside of docker)
1. Run `./src/summarize-topic-lengths.sh` (Linux only) to see how many characters each day's topic description has. If
   some description is suspiciously small or large, perhaps something was scraped and mistaken as the topic description.
1. View the topic descriptions in the respective files in `data` - i.e. `data/topics-2021.01.15.txt` for `2021.15.01`

If you have already downloaded the dataset and want to update the most recent days, then
run `local-download-data-latest.sh`. It will download all topics from `start-date` to today (or yesterday if none exists
for today).

### Automatic regular download

The `tagesschau-reloader` container is starts a cronjob, which downloads the newest data once per day at `20:00` UTC
time.

## Dataset

It was verified that the download of the topics text succeeds for all dates from `2014.01.01` to `2021.05.15`. Expected
failure dates are recorded in `config.yml` in `ignore-error-dates`. For these dates, en empty text is added
automatically.

## Development mode

Use `./restart-service dev` to start the docker containers in dev mode.

Additionally, if you want to manually start or stop containers using `docker-compose`, you first need
to `source config/source.sh`.

## Web Frontend

The frontend is written with NodeJS, NPM and Vue. In dev mode the `web/src` folder is mounted so that changes in the src
folder are compiled and hot-reloaded into the development web server. The frontend is served via nginx inside a docker container in production.

## Notes

Python is invoked with the `-u` option inside the docker container to provide immediate stdout prints as otherwise the
buffering may confuse a user who downloads the data.