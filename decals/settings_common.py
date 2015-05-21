"""
Django settings for decals project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

MAX_NATIVE_ZOOM = 15

ROOT_URL = '/viewer'
HOSTNAME = 'legacysurvey.org'
SUBDOMAINS = ['a','b','c','d']

STATIC_URL = 'http://%s%s/static/' % (HOSTNAME, ROOT_URL)

TILE_URL = 'http://{s}.%s%s/{id}/{ver}/{z}/{x}/{y}.jpg' % (HOSTNAME, ROOT_URL)

STATIC_TILE_URL = 'http://{s}.legacysurvey.org/static/tiles/{id}/{ver}/{z}/{x}/{y}.jpg'

CAT_URL = 'http://{s}.%s%s/{id}/{ver}/{z}/{x}/{y}.cat.json' % (HOSTNAME, ROOT_URL)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)
WEB_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(WEB_DIR, 'data')

#DUST_DIR = '/data1/SFD'
#DUST_DIR = '/project/projectdirs/desi/software/edison/dust/v0_0'
DUST_DIR = os.path.join(DATA_DIR, 'dust')
UNWISE_DIR = os.path.join(DATA_DIR, 'unwise-coadds')

#DUST_DIR = '/project/projectdirs/cosmo/webapp/viewer/dust'
#UNWISE_DIR = '/project/projectdirs/cosmo/data/unwise/unwise-coadds'


#os.environ['DECALS_DIR'] = '/project/projectdirs/cosmo/webapp/viewer/decals-edr/'
os.environ['DECALS_DIR'] = '/project/projectdirs/cosmo/webapp/viewer/decals-dr1/'




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=md&+t5!i#+%fd71_)cidw-&4ia%%0jr+5bh(_-8w(jm0d-v!='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (os.path.join(WEB_DIR, 'templates'),)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
#    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
#    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'decals.urls'

WSGI_APPLICATION = 'decals.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(WEB_DIR, 'static'),
)

STATIC_ROOT = os.path.join(WEB_DIR, 'static')

#print 'STATIC_ROOT is', STATIC_ROOT
