import yaml

CONFIG="config.yml"

def read_config():
  with open(CONFIG,"r") as file:
    return yaml.load(file, Loader=yaml.FullLoader)

d = read_config()
