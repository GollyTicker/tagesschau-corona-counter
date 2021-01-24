import traceback
import json
from datetime import datetime
from urllib.parse import *
from http.server import *

from shared import d, next_day, filename_for_date

def run_http_server():
  server_address = ("localhost", d["http-listen-port"])
  httpd = HTTPServer(server_address, FindHandler)
  httpd.serve_forever()

class FindHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    path_prefix = d["find-path"]+"/"
    if self.path.startswith(path_prefix):
      path_rest = self.path[len(path_prefix):]

      try:
        params = extract_parameters(path_rest)
        array = compute_result_array(params)
        self.response_ok_array(array)
      except Exception as e:
        traceback.print_exc()
        self.send_error(400)

    else:
      self.send_error(404)

  def response_ok_array(self, array):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps({"result":array}).encode())


def compute_result_array(params):
  current = params["start"]
  result = []
  while current <= params["end"]:
      result.append( day_contains_term(current,params["term"]) )
      current = next_day(current)
  print("Result:",result)
  return result

def day_contains_term(date, term):
  with open(filename_for_date(date),"r") as f:
      return term in f.read()

def extract_parameters(rest):
  components = urlparse(rest)
  dates = parse_qs(components.query,strict_parsing=True)

  search_term = components.path
  start_str = dates["start"][0]
  end_str = dates["end"][0]
  start = datetime.strptime(start_str, d["http-date-format"])
  end = datetime.strptime(end_str, d["http-date-format"])

  params = {"term": search_term, "start": start, "end": end}
  print("Parameters:",params)
  return params


if __name__ == "__main__":
    run_http_server()
