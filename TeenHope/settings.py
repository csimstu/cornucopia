# Django settings for TeenHope project.
import os
from django.core.urlresolvers import reverse
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

# Email Server Settings Here
EMAIL_HOST = "smtp.126.com"
EMAIL_HOST_USER = "majiallx@126.com"
EMAIL_HOST_PASSWORD = "2192716"
EMAIL_USE_TLS = True

MANAGERS = ADMINS

PROJECT_PATH = os.path.join(os.path.dirname(__file__), os.pardir)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'database', 'db.sqlite3'), # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Chongqing'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static_root')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dvhzbv!-3vs9p6ffv$!6pz30gv!aus&+&tqtx1^^+o)+5+zqbb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.templates.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TeenHope.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'TeenHope.wsgi.application'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\', '/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'forum',
    'accounts',
    'pages',
    'xadmin',
    'network',
    'widget_tweaks', # a plugin for conveniently adding css to widgets
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Customized settings below
AUTH_PROFILE_MODULE = "accounts.Profile"

# add a request variable in each template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Forum constants

TOPIC_PER_PAGE = 5
POST_PER_PAGE = 5
USERNAME_LENGTH_LIMIT = 20
PROFILE_NAME_LENGTH_LIMIT = 20
CATEGORY_TITLE_LENGTH_LIMIT = 50
CATEGORY_LABEL_LENGTH_LIMIT = 20
CATEGORY_DESCRIPTION_LENGTH_LIMIT = 200
TOPIC_TITLE_LENGTH_LIMIT = 50
POST_LENGTH_LIMIT = 10000
REPLY_LENGTH_LIMIT = 500

# Accounts constants
WEBSITE_LENGTH_LIMIT = 50
RENREN_LENGTH_LIMIT = 50
QQ_LENGTH_LIMIT = 20
PHONE_LENGTH_LIMIT = 20
BIOGRAPHY_LENGTH_LIMIT = 200
MOTTO_LENGTH_LIMIT = 50
GROUP_NAME_LENGTH_LIMIT = 50

DEFAULT_USER_THUMBNAIL = os.path.join(STATIC_URL, 'accounts', 'default_portrait.jpg')

# Pages constants
TAG_LENGTH_LIMIT = 50
ARTICLE_TITLE_LENGTH_LIMIT = 50
ARTICLE_LENGTH_LIMIT = 50000
ABSTRACT_LENGTH_LIMIT = 1000
COMMENT_LENGTH_LIMIT = 500

# Network constatns
MESSAGE_LENGTH_LIMIT = 10000
MESSAGE_SUBJECT_LENGTH_LIMIT = 100
TRACE_DESCRIPTION_LENGTH_LIMIT = 100
URL_LENGTH_LIMIT = 50

MAX_GROUPNAME_LENGTH = 100
CKBOX_SESSION_NAME = "check box"

# Validation regex
USERNAME_PATTERN = r'[A-Za-z]\w{5,19}' # regex for username, 6<=len<=20 with leading alpha
USERNAME_HINT = "Username must consist of 6 to 20 alpha or digits with leading alpha."
PASSWORD_PATTERN = r'\w{6,20}' # regex for username, 6<=len<=20
PASSWORD_HINT = "Password must consist of 6 to 20 alpha or digits."
EMAIL_PATTERN = r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*'
NICKNAME_PATTERN = r'[\w ]{6,20}'
WEBSITE_PATTERN = r'.{6,20}'

# Login url
LOGIN_URL = '/accounts/login/'


# Modify django message system
from django.contrib import messages

MESSAGE_TAGS = {
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: '',
    messages.ERROR: 'alert-error',
}

