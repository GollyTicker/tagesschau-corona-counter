from http.server import *

from shared import d

class FindHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.startswith(d["find-path"]+"/"):
      print("Got:",self.path)
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write("{\"SomeTestContent\":[1,2,3]}".encode())
    else:
      self.send_error(404)

server_address = ("localhost", d["http-listen-port"])
httpd = HTTPServer(server_address, FindHandler)
httpd.serve_forever()
