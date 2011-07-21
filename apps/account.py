import tornado.web
from tbone.user import get_user, orm, dummy_user


class AccountHandler(tornado.web.RequestHandler):
    def get(self):
        user = get_user(self,orm.Session())
        if user is None:
            user = dummy_user
        self.render('account.html',title='Account', greeting='Heyehey',
                user=user)

urls = [('',AccountHandler)]
