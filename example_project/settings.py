import os
import sys

def getpath(*paths):
    return os.path.abspath(os.path.join(*paths))

# ===== #
# PATHS #
# ===== #

PROJECT_ROOT = os.path.dirname(__file__)
RICHTEMPLATES_ROOT = getpath(PROJECT_ROOT, '..', 'richtemplates')
sys.path.insert(0, getpath(RICHTEMPLATES_ROOT, '..'))

MEDIA_ROOT = getpath(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'

# ======== #
# DATABASE #
# ======== #

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '.hidden.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# If enine is set to sqlite3 and name for db is not given
# as absolute path, it should be relative to environment
if DATABASE_ENGINE == 'sqlite3' and not DATABASE_NAME.startswith(':'):
    DATABASE_NAME = getpath(PROJECT_ROOT, DATABASE_NAME)

# ============== #
# BASIC SETTINGS #
# ============== #

ROOT_URLCONF = 'example_project.urls'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_L10N = True
LOGIN_REDIRECT_URL = '/'
SECRET_KEY = 'g==ps7az_^^5vn-bty+&o231kh)ei(xzvrikp6i#&7=q9htof1'
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.webdesign',

    'djalog',
    'django_sorting',
    'pagination',
    'registration',
    'rosetta',

    'richtemplates',
    'richtemplates.examples',

    'example_project',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'richtemplates.middleware.Http403Middleware',
    'django_sorting.middleware.SortingMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_DIRS = (
    getpath(PROJECT_ROOT, 'templates'),
)

# =============== #
# DJALOG SETTINGS #
# =============== #

DJALOG_SQL = False
DJALOG_SQL_LEVEL = 5
DJALOG_USE_COLORS = True
DJALOG_LEVEL = 20 # logging.INFO default level
DJALOG_FORMAT = '[%(levelname)s] %(message)s'

if DEBUG:
    DJALOG_SQL = True
    DJALOG_LEVEL = 5

try:
    import djalog
    INSTALLED_APPS += ('djalog',)
    if DJALOG_SQL:
        MIDDLEWARE_CLASSES += (
            'djalog.middleware.SQLLoggingMiddleware',
        )
except ImportError:
    pass

# ====================== #
# RICHTEMPLATES SETTINGS #
# ====================== #

RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES = {
    'code-block': 'richtemplates.rstdirectives.pygments_directive',
}
