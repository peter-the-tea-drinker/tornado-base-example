import sys, os
INTERP = os.path.expanduser("~/env/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)


#import sys,os.path
#sys.path.append(os.path.expanduser('~/tornado-base'))
#from base.passenger_wsgi_base import *

import tornado.ioloop
import tornado.web
import tornado.wsgi

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")

urls = [(r"/", HelloHandler)]
application = tornado.wsgi.WSGIApplication(urls)

