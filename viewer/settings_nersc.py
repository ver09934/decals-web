from viewer.settings_common import *

DEBUG = True

DEBUG_LOGGING = True

READ_ONLY_BASEDIR = True

USER_QUERY_DIR = '/tmp/viewer-user'

STATIC_TILE_URL_B = 'http://{s}.imagine.legacysurvey.org/static/tiles/{id}/{ver}/{z}/{x}/{y}.jpg'
SUBDOMAINS_B = SUBDOMAINS

# no CORS -- so don't use subdomains, or specify hostname (www.legacysurvey.org vs legacysurvey.org)
CAT_URL = '%s/{id}/{ver}/{z}/{x}/{y}.cat.json' % (ROOT_URL)

#ENABLE_CUTOUTS = True
#ENABLE_VCC  = False
#ENABLE_WL   = False
ENABLE_DR5  = True
#ENABLE_DR6  = True
#ENABLE_DES_DR1 = True
