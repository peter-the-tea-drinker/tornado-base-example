import sqlalchemy
import tornado.web
class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', title='A lean, mean kickstarter for Tornado.')

urls = [(r"/", HelloHandler)]

def add_urls(prefix,module_urls):
    for (url, handler) in module_urls:
        urls.append((prefix+url, handler))

import apps
add_urls (r'/account',apps.account.handlers.urls)
import apps.about
add_urls (r'/about',apps.about.handlers.urls)
import blog.blog
add_urls(r'/weblog',blog.blog.urls)
from base import handlers, user
add_urls('',handlers.urls)
from mp import TestHandler
urls.append((r"/test",TestHandler))


def make_fixtures():
    from base.appbase import orm
    blog.blog.make_fixtures() # has a unicode warning?
    user.make_fixtures()

