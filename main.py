import sqlalchemy
import tornado.web

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world! <a href="weblog/">The weblog</a>')

urls = [(r"/", HelloHandler)]

def add_urls(prefix,module_urls):
    for (url, handler) in module_urls:
        urls.append((prefix+url, handler))

import apps.blog.blog
add_urls(r'/weblog',apps.blog.blog.urls)
from base import user
add_urls('',user.urls)

def make_fixtures():
    from base.appbase import orm
    apps.blog.blog.make_fixtures()
    user.make_fixtures()

