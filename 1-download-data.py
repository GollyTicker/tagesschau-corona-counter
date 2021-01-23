import requests
import yaml
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup

CONFIG="config.yml"
d = {} # configuration from config.yaml

def main():
    global d
    d = read_config()

    start, end = read_start_and_end_date()

    after_end = next_day(end)

    current = start
    while not same_date(current, next_day(end)):
        # TODO: redirect stdout and stderr to log-files

        print("Getting topics for date", current)
        date_url = per_date_url(current)

        date_html = download_html_for(date_url)

        subpage_url = extract_url_to_subpage(date_html)

        sub_html = download_html_for(subpage_url)

        topics = extract_topics_of_show(sub_html)

        save_topics_to_disk(topics, current)

        current = next_day(current)


def read_config():
    with open(CONFIG,"r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def read_start_and_end_date():
    start = datetime.strptime(d["start-date"], d["date-format"])
    end = datetime.strptime(d["end-date"], d["date-format"])
    return (start, end)

def next_day(date):
    return date + timedelta(days = 1)

def same_date(dta, dtb):
    return dta.strftime("%Y-%m-%d") == dtb.strftime("%Y-%m-%d")

# date: datetime object
def per_date_url(date):
    date_str_for_url = date.strftime(d["per-date-path-format"])
    # replace keyword in URL with the upper date to get the full url
    path =  d["per-date-path"].replace(d["per-date-path-keyword"],date_str_for_url)
    return d["base-url"] + path


def download_html_for(url):
    print("GET", url)
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def extract_url_to_subpage(html):
    navigator = BeautifulSoup(html,"html.parser")

    # findAll: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
    links = navigator.findAll(name="a",string=d["per-date-search-for-subpage"])

    # there should be exactly one taggesschau per day:
    error_on_empty(links,"anchor link to subpage")
    warn_on_more_than_one(links,"anchor link to subpage")

    subpage_path = links[0]["href"] # to config?
    subpage_url = d["base-url"] + subpage_path
    print("Extracted subpage url:",subpage_url)

    return subpage_url

def warn_on_more_than_one(results, elt_description):
    if len(results) >= 2:
        print("WARNING: Found multiple " + elt_description)

def error_on_empty(results, elt_description):
    if len(results) == 0:
        print("ERROR: " + elt_description + "not found!")
        raise ValueError

def extract_topics_of_show(html):
    navigator = BeautifulSoup(html, "html.parser")

    print("Looking for content element.")
    main = navigator.find(name="div",class_="inhalt") # to config?
    # one would be best. usually there is mor. but first one is usually correct
    warn_on_more_than_one(main,"content element")
    error_on_empty(main, "content element")

    print("Looking for topics text.")
    # to config?
    teaserTexts = main.findAll(name="p",class_="teasertext")
    is_topic_p = lambda p: d["topics-text-discriminator"] in str(p.contents[0])
    get_text_from_p = lambda p: p.contents[1]
    topics_texts = [ get_text_from_p(p) for p in teaserTexts if is_topic_p(p) ]

    warn_on_more_than_one(topics_texts,"topics text")
    error_on_empty(topics_texts,"topics text")

    if topics_texts[0].strip() == "":
        print("ERROR: Topics text is empty!")
        raise ValueError

    return topics_texts[0]

def save_topics_to_disk(topics, date):
    filename = d["target-path-prefix"] + date.strftime(d["date-format"]) + d["target-path-suffix"]
    with open(filename,"w") as f:
        f.write(topics)
    print("Wrote topics to file:",filename)

if __name__ == "__main__":
    main()
