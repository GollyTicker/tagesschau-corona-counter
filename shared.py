import yaml
from datetime import timedelta
CONFIG = "config.yml"

def read_config():
  with open(CONFIG,"r") as file:
    return yaml.load(file, Loader=yaml.FullLoader)

def next_day(date):
  return date + timedelta(days = 1)

def filename_for_date(date):
    return d["data-path-prefix"] + date.strftime(d["date-format"]) + d["data-path-suffix"]

d = read_config()
