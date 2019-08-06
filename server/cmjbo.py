#!/bin/python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import time
import sys

SERVER_ROOT = '../html'

class CachedFile:

    def __init__(self, path):
        self.path = path
        self.mtime = -1
        self.get_contents()

    def __sizeof__(self):
        return len(self.contents) + sys.getsizeof(CachedFile)


    def needs_update(self):
        return self.mtime < os.path.getmtime(self.path)


    def get_contents(self):
        
        if self.needs_update():
        
            with open(self.path) as f:
                self.contents = f.read()

            self.mtime = time.time()

        return self.contents


    def set_contents(self, contents):
        
        self.contents = contents

        with open(self.path, 'w') as f:
            f.write(self.contents)

        self.mtime = time.time()

    def get_mimetype(self):
        # TODO
        self.mimetype = 'text/html'
        return self.mimetype


class Cache:

    def __init__(self):
        self._cache = dict()

    def get_file(self, path):
        if not self.contains(path):
            self.add_file(path)
        return self._cache[path]

    def contains(self, key):
        return key in self._cache

    def add_file(self, path):
        if not os.path.isfile(path):
            self._cache[path] = None
        else:
            cached_file = CachedFile(path)
            self._cache[path] = cached_file

    def add_alias(self, alias, path):
        self._cache[alias] = self._cache[path]

    def get_status(self):
        size = sys.getsizeof(self)
        return f"Cache size={size}"

    def __sizeof__(self):
        total = sys.getsizeof(Cache) + sys.getsizeof(dict)
        for path, fobj in self._cache.items():
            total += sys.getsizeof(fobj)
        return total

cache = Cache()
cache.add_file('../html/index.html')
cache.add_alias('../html/', '../html/index.html')


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        requested_file = cache.get_file(os.path.join(SERVER_ROOT, self.path[1:]))

        if requested_file == None:
            return self.file_not_found()

        self.serve_file(requested_file)


    def do_POST(self):
        pass


    def file_not_found(self):
        self.respond(400, 'text/html', '\n'.join([
                '<html>',
                '  <body>',
                '    <h1 style="text-align: center;">404</h1>',
                '  </body>',
                '</html>'
                ]))


    def serve_file(self, cached_file):

        self.respond(200, 
                cached_file.get_mimetype(),
                cached_file.get_contents())


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
