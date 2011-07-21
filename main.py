import sqlalchemy
import tornado.web
from tbone import user
from tbone import appbase
class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        session = appbase.orm.Session()
        user_obj = user.get_user(self,session)
        if user_obj is None:
            greeting = 'Welcome, please sign in here: '
        else:
            greeting = "Hi "+user_obj.name+"! "
        self.render('index.html', title='A lean, mean kickstarter for Tornado.',
                greeting= greeting
                )

urls = [(r"/", HelloHandler)]

def add_urls(prefix,module_urls):
    for (url, handler) in module_urls:
        urls.append((prefix+url, handler))

import apps
add_urls (r'/account',apps.account.urls)
import apps.about
add_urls (r'/about',apps.about.urls)
import blog.blog
add_urls(r'/weblog',blog.blog.urls)
from tbone import handlers, user
add_urls('',handlers.urls)
from tbone.run_async import TestHandler
urls.append((r"/test",TestHandler))


def make_fixtures():
    from tbone.appbase import orm
    blog.blog.make_fixtures() # has a unicode warning?
    user.make_fixtures()

