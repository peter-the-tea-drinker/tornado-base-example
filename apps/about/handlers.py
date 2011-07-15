import tornado.web
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('base.html',title='about')

class TermsHandler(AboutHandler): pass

class PrivacyHandler(TermsHandler): pass

class DCMAHandler(TermsHandler): pass

urls = [('/', AboutHandler),
        ('/terms', TermsHandler),
        ('/privacy', AboutHandler),
        ('/DCMA', AboutHandler),
        ]

