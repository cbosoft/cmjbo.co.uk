'''
database.py

Handles the storage and access of app data.
'''

import os
import json

# TODO replace with SQL
class Database(dict):
    '''
    Class object to retreive and store app data quickly and efficiently.
    '''


    DATA_DIR = '../data'


    def __init__(self, path):
        self.path = os.path.join(self.DATA_DIR, path)
        try:
            with open(self.path) as jsonf:
                data = json.load(jsonf)
        except FileNotFoundError:
            with open(self.path, 'w') as jsonf:
                json.dump({}, jsonf)
            data = dict()

        self.update(data)


    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()

    def __getitem__(self, key):
        if key not in self:
            self[key] = {'menukey': key, 'menu': [], 'list':[], 'sorted':[]}
        rv = super().__getitem__(key)
        return rv


    def save(self):
        '''
        Write database to disk
        '''

        with open(self.path, 'w') as jsonf:
            json.dump(self, jsonf)
