# see http://www.sqlalchemy.org/docs/core/engines.html#database-urls
# These are need on the server (so you need to add them)
import os,sys

VIRTUAL_ENV = "~/env/bin/python"

DB = 'sqlite:///:memory:'
BASE_DIR = '~/tornado-base'

COOKIE_SECRET ="CISFORCOO23ETHAT'SNO4546%$@GHFORMEOHLOOKSHINEYTHINGSISTHATENO"

ADMIN = 'peter.row@gmail.com'

sys.path.append(os.path.expanduser(BASE_DIR))

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

#settings = {
#        'google_consumer_key':None,
#        'google_consumer_secret':None,
#        'twitter_consumer_key':None,
#        'twitter_consumer_secret':None,
#        'facebook_consumer_key':None,
#        'facebook_consumer_secret':None
#        }
 
