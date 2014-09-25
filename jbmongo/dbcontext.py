# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

from .basedocument import BaseDocument
from pymongo import MongoClient

class DBContext(object):
    def __init__(self, host='localhost', port=27017, dbname='default_database'):
        self._mongo_client = MongoClient(host, port)
        self._database = self._mongo_client[dbname]

    def base_document(self):
        return type('Document', (BaseDocument, ), dict(database=self._database))