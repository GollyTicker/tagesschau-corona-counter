import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

from shared import d, next_day, write_file_for_date, n_days_before

def main():
    start, end = read_start_and_end_date()

    error_dates = read_error_dates()

    current = start
    while current <= end:
        try:
            print("=================\nGetting topics for date", current)
            date_url = per_date_url(current)
            date_html = download_html_for(date_url)
            subpage_url = extract_url_to_subpage(date_html)
            sub_html = download_html_for(subpage_url)
            topics = extract_topics_of_show(sub_html)
            save_topics_to_disk(topics, current)

        except:
            if current in error_dates:
                print("EXPECTED: Error for date",current,". Saving empty file to disk.")
                save_topics_to_disk("", current)
                pass
            else:
                raise # preserve prior trace

        finally:
            current = next_day(current)


def read_start_and_end_date():
    start = datetime.strptime(d["start-date"], d["date-format"])
    endstr = d["end-date"]
    end = get_latest_date() if endstr == "latest" else datetime.strptime(endstr, d["date-format"])
    return (start, end)

def get_latest_date():
    # If we are after 22:00 then we take today, as tagesschau will be uploaded
    # to archive already. Otherwise we take the previous day
    now = datetime.now().replace(tzinfo=timezone.utc)
    today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    time_of_upload = today.replace(hour=20,minute=50,tzinfo=timezone(timedelta(hours=1)))
    return today if time_of_upload <= now else n_days_before(1,today)

def read_error_dates():
    return [ datetime.strptime(date, d["date-format"]) for date in d["ignore-error-dates"] ]

# date: datetime object
def per_date_url(date):
    date_str_for_url = date.strftime(d["per-date-path-format"])
    # replace keyword in URL with the upper date to get the full url
    path = d["per-date-path"].replace(d["per-date-path-keyword"],date_str_for_url)
    return d["base-url"] + path


def download_html_for(url):
    print("GET", url)
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def extract_url_to_subpage(html):
    navigator = BeautifulSoup(html,"html.parser")

    # findAll: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
    allAnchors = navigator.findAll(name="a")

    anchor_is_link_to_subpage = lambda a: d["per-date-search-for-subpage"] == a.get_text(strip=True)
    links = [a for a in allAnchors if anchor_is_link_to_subpage(a)]

    # there should be exactly one taggesschau per day:
    error_on_empty(links,"anchor link to subpage")
    warn_on_more_than_one(links,"anchor link to subpage")

    subpage_path = links[0]["href"]
    subpage_url = d["base-url"] + subpage_path
    print("Extracted subpage url:",subpage_url)

    return subpage_url

def warn_on_more_than_one(results, elt_description):
    if len(results) >= 2:
        print("WARNING: Found multiple " + elt_description + f" [{len(results)}]")

def error_on_empty(results, elt_description):
    if len(results) == 0:
        print("ERROR: " + elt_description + " not found!")
        raise ValueError

def extract_topics_of_show(html):
    navigator = BeautifulSoup(html, "html.parser")

    print("Looking for content element.")
    main = navigator.find(name="div",class_="copytext__video__details")
    # one would be best. usually there is mor. but first one is usually correct
    warn_on_more_than_one(main,"content element")
    error_on_empty(main, "content element")

    print("Looking for topics text.")
    teaserTexts = main.findAll(name="p")
    warn_on_more_than_one(teaserTexts,"teaser text")
    error_on_empty(teaserTexts, "teaser text")

    text = teaserTexts[0].get_text(strip=True)

    if text == "":
        print("ERROR: Topics text is empty!")
        raise ValueError

    return text

def save_topics_to_disk(topics, date):
    filename = write_file_for_date(topics, date)
    print("Wrote topics to file:",filename)

if __name__ == "__main__":
    main()
