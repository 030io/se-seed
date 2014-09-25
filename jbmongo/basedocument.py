# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

class BaseDocument(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collection = None

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        return self[key]

    def save(self):
        return self.get_collection().save(self)

    @classmethod
    def get_collection(cls):
        return cls.database[cls.__name__]

    @classmethod
    def find_one(cls, *args, **kwargs):
        return cls(cls.get_collection().find_one(*args, **kwargs))

    @classmethod
    def find(cls, *args, **kwargs):
        return [cls(obj) for obj in cls.get_collection().find(*args, **kwargs)]

