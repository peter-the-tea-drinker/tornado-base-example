import config
import os,sys
sys.path.append(os.path.expanduser(config.LOCAL_APP_DIR))
sys.path.append(os.path.expanduser(config.LOCAL_BASE_DIR))

import base.fabbase

dev = base.fabbase.dev
test = base.fabbase.test
stage = base.fabbase.stage
prod = base.fabbase.prod

