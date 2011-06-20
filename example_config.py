# see http://www.sqlalchemy.org/docs/core/engines.html#database-urls
# These are need on the server (so you need to add them)
import os,sys

VIRTUAL_ENV = "~/virtualenv/bin/python"

DB = 'sqlite:///:memory:'
BASE_DIR = '~/base'

COOKIE_SECRET = "nobody should be able to guess this"

ADMIN = "me@example.com"

sys.path.append(os.path.expanduser(BASE_DIR))

# These are only needed by fab
APP_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base-example.git'
APP_TAG = ''

STAGE_APP_DIR = '~/stage.example.com'
PROD_APP_DIR = '~/prod.example.com'

BASE_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base.git'
BASE_TAG = ''

LOCAL_BASE_DIR = '~/tornado-base'
LOCAL_APP_DIR = '~/tornado-base-example'

sys.path.append(os.path.expanduser(LOCAL_APP_DIR))
sys.path.append(os.path.expanduser(LOCAL_BASE_DIR))
