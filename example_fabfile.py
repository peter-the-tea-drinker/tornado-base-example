import os,sys
sys.path.append(os.path.expanduser('~/repos/tornado-base'))
import base.fabbase

base.fabbase.APP_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base-example.git'
base.fabbase.APP_TAG = ''

base.fabbase.STAGE_APP_DIR = '~/stage.example.com'
base.fabbase.PROD_APP_DIR = '~/prod.eexample.com'

base.fabbase.BASE_DIR = '~/tornado-base'
base.fabbase.BASE_REPO = 'git://github.com/peter-the-tea-drinker/tornado-base.git'
base.fabbase.BASE_TAG = ''

stage = base.fabbase.stage
prod = base.fabbase.prod

