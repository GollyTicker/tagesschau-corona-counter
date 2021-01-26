import yaml
from datetime import timedelta

CONFIG = "config.yml"

def read_config():
    with open(CONFIG,"r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def next_day(date):
    return date + timedelta(days = 1)

def n_days_before(n,date):
    return date - timedelta(days = n)

def filename_for_date(date):
    return d["data-path-prefix"] + date.strftime(d["date-format"]) + d["data-path-suffix"]

def write_file_for_date(str, date):
    filename = filename_for_date(date)
    with open(filename,"w") as f:
        f.write(str)
    return filename

def read_file_for_date(date):
    with open(filename_for_date(date),"r") as f:
        return f.read()

d = read_config()
