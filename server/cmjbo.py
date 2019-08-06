#!/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.respond(200, "text/plain", "Hello, world!")

    def do_POST(self):
        pass

    def respond(self, code, mime, data):
        self.send_response(code)
        self.send_header('Content-type', mime)
        
        if isinstance(data, str):
            data = data.encode('utf-8')

        self.wfile.write(data)


httpd = HTTPServer( ('', 80), Handler)

if os.fork() == 0:
    httpd.serve_forever()
else:
    print("Server forked to background.")
