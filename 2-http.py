import traceback
import json
from datetime import datetime
from urllib.parse import *
from http.server import *

from shared import d, next_day, read_file_for_date

def run_http_server():
    server_address = ("localhost", d["http-listen-port"])
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        find_path_prefix = d["find-path"]+"/"
        text_path_prefix = d["text-path"]

        # /find/<term>?start=<date>&end=<date>
        if self.path.startswith(find_path_prefix):
            path_rest = self.path[len(find_path_prefix):]
            self.with_exceptions_as_http(process_find_request,[path_rest])

        # /file/<date>
        elif self.path.startswith(text_path_prefix):
            path_rest = self.path[len(text_path_prefix):]
            self.with_exceptions_as_http(process_text_request, [path_rest])
        else:
            self.send_error(404)

    def with_exceptions_as_http(self, func, args=[],kwargs={}):
        try:
            result = func(*args,**kwargs)
            self.response_ok(result)
        except Exception as e:
            traceback.print_exc()
            self.send_error(400)

    def response_ok(self, result):
        jsonBody = json.dumps({"result":result})
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(jsonBody.encode())

def process_text_request(path_rest):
    start, end = extract_start_end_dates(path_rest)
    result = []
    current = start
    while current <= end:
        result.append( read_file_for_date(current) )
        current = next_day(current)
    print("Result with",len(result),"elements.")
    return result

def process_find_request(path_rest):
    params = extract_parameters(path_rest)
    return compute_result_array(params)


def compute_result_array(params):
    current = params["start"]
    result = []
    while current <= params["end"]:
        result.append( day_contains_term(current,params["term"]) )
        current = next_day(current)
    print("Result:",result)
    return result

def day_contains_term(date, term):
    return term in read_file_for_date(date)

def extract_start_end_dates(path):
    components = urlparse(path)
    dates = parse_qs(components.query,strict_parsing=True)
    start_str = dates["start"][0]
    end_str = dates["end"][0]
    start = datetime.strptime(start_str, d["http-date-format"])
    end = datetime.strptime(end_str, d["http-date-format"])
    return (start, end)

def extract_parameters(rest):
    search_term = urlparse(rest).path
    start, end = extract_start_end_dates(rest)
    params = {"term": search_term, "start": start, "end": end}
    print("Parameters:",params)
    return params


if __name__ == "__main__":
    run_http_server()
