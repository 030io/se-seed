# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

from tornado.testing import AsyncHTTPTestCase
from simpleweb import application
import json

class SimpleWebTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return application

    def test_simple(self):
         response = self.fetch('/simplejson')
         data = json.loads(response.body.decode('utf-8'))
         self.assertIn('name', data)
         self.assertEqual(data['name'], 'Chinfeng Chung')
         self.assertEqual(data['characteristics'], 'handsome')