# -*- coding: utf-8 -*-
__author__ = 'chinfeng'

import tornado.web

class SimpleJsonHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(dict(
            name='Chinfeng Chung',
            characteristics='handsome',
        ))

application = tornado.web.Application([
    (r"/simplejson", SimpleJsonHandler),
])
