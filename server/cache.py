'''
cache.py

Provides a Cache class and a CachedFile class, one is a collection of the other.
If a file is requested that is not in the cache, it is added.

TODO: LRU cache
TODO: exclude alias files from LRU
'''
import os
import time
import sys
import mimetypes




class CachedFile:
    '''
    A CachedFile object is a file that is held in memory unless the disk
    version is newer.
    '''

    def __init__(self, path):
        self.path = path
        self.mtime = -1
        self.contents = []

        self.get_contents()


    def __sizeof__(self):
        return len(self.contents) + sys.getsizeof(CachedFile)


    def needs_update(self):
        '''
        Returns whether the file is out-of-date with respect to the filesystem
        or not.
        '''

        return self.mtime < os.path.getmtime(self.path)


    def get_contents(self):
        '''
        Returns the contents of the file, updating from disk if need be.
        '''

        if self.needs_update():

            with open(self.path) as f:
                self.contents = f.read()

            self.mtime = time.time()

        return self.contents


    def set_contents(self, contents):
        '''
        Set new contents to the file. This also overwrites the file on the disk,
        even if the disk file is newer (warning in that case however).

        I don't expect the disk files to ever, really, be newer. The only source
        for files getting written should be this script, so if another source
        has written to a file, it is probably a mistake.
        '''

        if self.needs_update():
            pass # TODO warning

        self.contents = contents

        with open(self.path, 'w') as f:
            f.write(self.contents)

        self.mtime = time.time()


    def get_mimetype(self):
        '''
        Returns mimetype of file.
        '''

        guessed_mimetype = mimetypes.guess_type(self.path, False)
        # returns either the type (str) or (type, encoding) tuple

        if isinstance(guessed_mimetype, str):
            return guessed_mimetype

        return guessed_mimetype[0]




class Cache(dict):
    '''
    A collection of CachedFile (dict)
    '''


    def __getitem__(self, path):
        '''
        Returns a CachedFile object from the cache. If the file is not in the
        cache, file is read in from filesystem.

        If file is not in either cache or filesystem, return None
        '''

        if not path in self:
            self.add_file(path)

        return super().__getitem__(path)


    def __sizeof__(self):
        total = sys.getsizeof(Cache) + sys.getsizeof(dict)
        for dummy, fobj in self.items():
            total += sys.getsizeof(fobj)
        return total


    def add_file(self, path):
        '''
        Add a file to the cache, checking if it exists. If it doesn't, None is
        added to the cache instead.
        '''

        if not os.path.isfile(path):
            self[path] = None
        else:
            cached_file = CachedFile(path)
            self[path] = cached_file


    def add_alias(self, alias, path):
        '''
        Add an alias, so that a different path may point to the same file.
        '''
        if path in self:
            self[alias] = self[path]
        else:
            pass # TODO warn


    def get_status(self):
        '''
        Get the status of the cache (some statistics etc) as a str.
        '''

        size = sys.getsizeof(self)
        return f"Cache size={size}"
