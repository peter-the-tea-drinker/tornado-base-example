import config
from base.user import get_user
from base.appbase import orm
import sqlalchemy as s

class Blog(orm.Base):
    __tablename__ = 'blog'
    id = s.Column(s.Integer, primary_key=True)
    #html = Column(UnicodeText)
    title = s.Column(s.String(50))
    slug = s.Column(s.String(50),unique=True)
    html = s.Column(s.Text)
    def __init__(self, title, html, slug = None):
        import tornado.escape
        self.html = html
        self.title = title
        if slug is None:
            slug = tornado.escape.url_escape(title)
        self.slug = slug
    def __repr__(self):
        return str(self.html)

import tornado.web
class BlogIndex(tornado.web.RequestHandler):
    def get(self):
        #self.write('hih')
        blogs = [b for b in orm.Session().query(Blog).all()]#['1','2']
        user = get_user(self,orm.Session())
        name = 'Anonymous' if user is None else user.name
        self.render("blogindex.html",blogs = blogs,
                name=name,path=self.request.path)

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("title") + self.get_argument("message"))

# page = ?


class BlogHandler(tornado.web.RequestHandler):
    def get(self,entry):
        import tornado.escape
        #slug = tornado.escape.url_unescape(entry)
        slug = tornado.escape.url_escape(entry.decode('utf-8'))
        post = orm.Session().query(Blog).filter_by(slug=slug).first()
        self.write('''<html><body>%s
                    <form action="%s" method="post">
                    <input type="text" name="message">
                    <input type="submit" value="Submit">
                    </form></html></body>'''%(post,self.request.path))

    def post(self,entry):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))


urls =  [
        (r"/",BlogIndex),
        (r"/(.+)", BlogHandler),
        ]

def make_fixtures():
    # Warning, only call this once, or it will crash (due to duplicate entries)
    # Note, text.get_app() is called every unit test, so DON'T do this:

    # class TestBlog(AsyncHTTPTestCase):
    #    def get_app(self):
    #        blog.make_fixtures() # BAD!
    #        return Application(blog.urls)

    nihao = u'\u4f60\u597d' # Chinese for "hello" to test unicode.
    # u.encode('ascii', 'xmlcharrefreplace')? 
    orm.Base.metadata.create_all(orm.engine)
    session = orm.Session()

    first_post = Blog('First','I IZ IN UR DATABASE, DROPPNI UR TBALEZ!'+1000*' '+'KTHXBYE')
    session.add(first_post)
    second_post = Blog('Second','I IZ STILL IN UR DATABASE')
    session.add(second_post)
    uni = Blog(nihao,'unicode '*100)
    session.add(uni)

    session.commit()
    post = session.query(Blog).first()
    # how is unicode title handled?
    # are capitals unique?
    # blank title?

