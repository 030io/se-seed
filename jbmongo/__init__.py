# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

class BaseDocument(object):
    def save(self):
        return NotImplemented

    @classmethod
    def find_one(cls, *args, **kwargs):
        return dict(_id=1)

class DBContext(object):
    def base_document(self):
        return BaseDocument