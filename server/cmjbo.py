#!/bin/python3
'''
cmjbo.py

Server code for my website (http://cmjbo.co.uk). This python code responds to
GET requests for pages, and to POST requests exchanging data between apps on the
site and the server filesystem.
'''

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

from cache import Cache
from shopping_list_app import shopping_process




class Handler(BaseHTTPRequestHandler):
    '''Handles HTTP requests, responding to GET requests with the relevent page,
    or 404, and to POST with application data.'''


    ROOT = '../html'


    def __init__(self, *args, **kwargs):
        self.cache = Cache()
        self.cache.add_file('../html/index.html')
        self.cache.add_alias('../html/', '../html/index.html')

        self.apps = dict()
        self.apps['/shopping_list'] = shopping_process

        super().__init__(*args, **kwargs)


    def do_GET(self):
        '''
        Respond to GET request.

        A GET request shopuld be asking for a page or other document on the
        server, it should be a file that exists. If it is, send it back.
        Otherwise, send a "404: file not found" page.
        '''

        requested_file = self.cache[os.path.join(self.ROOT, self.path[1:])]

        if requested_file is None:
            self.file_not_found()
        else:
            self.serve_file(requested_file)


    def do_POST(self):
        '''
        Handle POST request.
        '''

        content_length = int(self.headers['Content-length'])
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        if self.path in self.apps:
            self.respond(200, 'application/json', self.apps[self.path](data))
        else:
            self.file_not_found()


    def file_not_found(self):
        '''
        Returns a 404 page to client if requested file is not found.
        '''

        self.respond(400, 'text/html', '\n'.join([
            '<html>',
            '  <body>',
            '    <h1 style="text-align: center;">404</h1>',
            '  </body>',
            '</html>'
        ]))


    def serve_file(self, cached_file):
        '''
        Convenience func to send file to client.
        '''

        self.respond(
            200,
            cached_file.get_mimetype(),
            cached_file.get_contents())


    def respond(self, code, mime, data):
        '''
        Send response to client.
        '''

        self.send_response(code)
        self.send_header('Content-type', mime)

        if isinstance(data, str):
            data = data.encode('utf-8')

        self.wfile.write(data)



HTTPD = HTTPServer(('', 80), Handler)
print("Starting server")
HTTPD.serve_forever()
