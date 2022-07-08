import json
import os
import traceback
from datetime import datetime
from http.server import *
from urllib.parse import *

import numpy as np

from shared import d, next_day, read_file_for_date, n_days_before

FIND_PATH_PREFIX = d["find-path"] + "/"
TEXT_PATH_PREFIX = d["text-path"]
SUM_PATH_PREFIX = d["sum-path"] + "/"

data = {}

def run_http_server():
    server_address = ("0.0.0.0", d["api-port-internal"])
    httpd = HTTPServer(server_address, Handler)
    print(f"Serving at {server_address}")
    httpd.serve_forever()

# HTTP requests handler
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path.startswith(FIND_PATH_PREFIX):
            path_rest = self.path[len(FIND_PATH_PREFIX):]
            self.with_exceptions_as_http(process_find_request, [path_rest])

        elif self.path.startswith(TEXT_PATH_PREFIX):
            path_rest = self.path[len(TEXT_PATH_PREFIX):]
            self.with_exceptions_as_http(process_text_request, [path_rest])

        elif self.path.startswith(SUM_PATH_PREFIX):
            path_rest = self.path[len(SUM_PATH_PREFIX):]
            self.with_exceptions_as_http(process_sum_request, [path_rest])

        else:
            self.send_error(404)

    def with_exceptions_as_http(self, func, args=[], kwargs={}):
        try:
            result = func(*args, **kwargs)
            self.response_ok(result)
        except Exception as e:
            traceback.print_exc()
            self.send_error(400)

    def response_ok(self, result):
        jsonBody = json.dumps({"result": result})
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(jsonBody.encode())


# sum request
def process_sum_request(path_rest):
    term, N, start, end = extract_sum_request_parameters(path_rest)
    if N < 1:
        raise ValueError(f"n = {N} be >= 1.")
    array = compute_binary_occurrence_array(term, n_days_before(N - 1, start), end)
    scan_sum = scansum(N, to_np_array(bool, array))
    print(f"Result: {scan_sum}")
    return to_py_list(int, scan_sum)


def to_np_array(type, py_list):
    return np.array(py_list, dtype=np.dtype(type))


def to_py_list(type, nparray):
    return list(map(type, nparray))


def extract_sum_request_parameters(rest):
    search_term = urlparse(rest).path
    start, end = extract_start_end_dates(rest)
    N = int(parse_qs(urlparse(rest).query, strict_parsing=True)["n"][0])
    return (search_term, N, start, end)


#   scansum(3,[a,  b,    c,     d,     e])
# =                 [a+b+c, b+c+d, c+d+e]
# fast O(n) N-element scansum
# using a sliding algorithm where a+b+c -> b+c -> b+c+d in each iteration.
def scansum(N, a):
    L = len(a) - (N - 1)
    result = np.zeros(L, dtype=np.int)
    s = 0
    for i in range(len(a)):
        s = s + a[i]
        di = i - (N - 1)
        if di >= 0:
            result[di] = s
            s = s - a[di]

    print(f"scansum({N}, len(a)={len(a)}) => len(result) = {len(result)}")
    return result


# text request
def process_text_request(path_rest):
    start, end = extract_start_end_dates(path_rest)
    result = []
    current = start
    while current <= end:
        result.append(get_topics_for_date(current))
        current = next_day(current)
    print("Result with", len(result), "elements.")
    return result


# find request
def process_find_request(path_rest):
    params = extract_find_parameters(path_rest)
    array = compute_binary_occurrence_array(**params)
    print("Result:", array)
    return array


def extract_find_parameters(rest):
    search_term = urlparse(rest).path
    start, end = extract_start_end_dates(rest)
    params = {"term": search_term, "start": start, "end": end}
    print("Parameters:", params)
    return params


# utilities shared by the requests
def compute_binary_occurrence_array(term, start, end):
    current = start
    result = []
    while current <= end:
        result.append(day_contains_term(current, term))
        current = next_day(current)
    return result


def day_contains_term(date, term):
    return term in get_topics_for_date(date)


def extract_start_end_dates(path):
    components = urlparse(path)
    dates = parse_qs(components.query, strict_parsing=True)
    start_str = dates["start"][0]
    end_str = dates["end"][0]
    start = datetime.strptime(start_str, d["http-date-format"])
    end = datetime.strptime(end_str, d["http-date-format"])
    return (start, end)


def load_data_into_memory():
    print("Loading data into memory...")
    topic_files = all_files_in_data()
    for file in topic_files:
        date = extract_date_from_file_name(file)
        date_string = date.strftime(d["date-format"])
        data[date_string] = read_file_for_date(date)
    print("Loaded", len(topic_files), "dates.")


def get_topics_for_date(date):
    date_string = date.strftime(d["date-format"])
    return data[date_string]


def extract_date_from_file_name(name):
    date_string = name[len(d["data-file-prefix"]):][:-len(d["data-path-suffix"])]
    return datetime.strptime(date_string, d["date-format"])


def all_files_in_data():
    all_files = os.listdir(d["data-folder"])
    return [
        file for file in all_files
        if file.startswith(d["data-file-prefix"])
           and file.endswith(d["data-path-suffix"])
    ]


# main
if __name__ == "__main__":
    load_data_into_memory()
    run_http_server()
