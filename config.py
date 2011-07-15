# see http://www.sqlalchemy.org/docs/core/engines.html#database-urls
# These are need on the server (so you need to add them)
import os,sys

VIRTUAL_ENV = "~/env/bin/python"

DB = 'sqlite:///:memory:'
BASE_DIR = '~/tornado-base'

COOKIE_SECRET ="CISFORCOO23ETHAT'SNO4546%$@GHFORMEOHLOOKSHINEYTHINGSISTHATENO"
BCRYPT_SALT = '$2a$12$pmo745pf7A.t164vP2pTle'

ADMIN = 'peter.row@gmail.com'

sys.path.append(os.path.expanduser(BASE_DIR))

STATIC = os.path.join(os.path.dirname(__file__),'static')

#email_domain = 'peter-the-tea-drinker.com'
#email_server = 'dummy'#'mail.peter-the-tea-drinker.com'
#email_user = 'pete@peter-the-tea-drinker.com'
#email_password = 'Kl8ySfWIJRLX6TNfEBlujATzl'
#email_secure = True
email_domain = 'gmail.com'
#email_server = 'smtp.gmail.com'
email_server = 'dummy'
email_user = 'peter.row@gmail.com'
email_password = 'doyouhearthepeoplesing'
email_secure = True

magic_token_url='peter-the-tea-drinker.com/m/'

TEMPLATE = os.path.join(os.path.dirname(__file__),'template')


# These are only needed by fab
APP_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base-example.git'
APP_TAG = ''

PROD_APP_DIR = '~/peter-the-tea-drinker.com'
STAGE_APP_DIR = '~/peter-the-tea-drinker.com'

BASE_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base.git'
BASE_TAG = ''

LOCAL_BASE_DIR = '~/repos/tornado-base'
LOCAL_APP_DIR = '~/repos/tornado-base-example'

sys.path.append(os.path.expanduser(LOCAL_APP_DIR))
sys.path.append(os.path.expanduser(LOCAL_BASE_DIR))

# global RECAPTCHA keys, from https://www.google.com/recaptcha/admin/create
# don't use them. Make your own. These are just for development. 
PUBLIC_RE_KEY = '6LccF8YSAAAAAL1OzoFUMq4gOSjnndh4rl62uH5c'
PRIVATE_RE_KEY = '6LccF8YSAAAAAKX28tyU9imyorOYTE4-CET8fygZ'

#settings = {
#        'google_consumer_key':None,
#        'google_consumer_secret':None,
#        'twitter_consumer_key':None,
#        'twitter_consumer_secret':None,
#        'facebook_consumer_key':None,
#        'facebook_consumer_secret':None
#        }
 
