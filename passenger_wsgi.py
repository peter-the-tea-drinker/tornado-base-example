import config
INTERP = os.path.expanduser(config.VIRTUAL_ENV)
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
import main, base.appbase
application = base.appbase.wsgi_app(main.urls,cookie_secret=config.COOKIE_SECRET)

