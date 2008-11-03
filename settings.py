# Django settings for Ochs project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

IMAGE_UPLOAD_PATH = ""
IMAGE_FILE_PATH = ""
SIZE_THUMBNAIL = 90, 90
SIZE_RESIZE = 512, 640
SIZE_SIDEBAR = 220, 360
SIZE_BOX = 780, 480
SIZE_STORY02 = 240, 600
SIZE_HOME04 = 758, 600

ADMINS = (
    ('Operations', 'errors@tnjn.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'EST5EDT'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

SESSION_COOKIE_NAME = "tnjn"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

USE_I18N = True

MEDIA_ROOT = ''
MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/admin/'

CACHE_MIDDLEWARE_SECONDS = 600
CACHE_BACKEND = "memcached://127.0.0.1:11211"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

SECRET_KEY = 'h%_qy_a#-8_b=5jgk^muldv8ah6-8we=-^-yd$pdb1f#ac8h14'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'tnjn.urls'

TEMPLATE_DIRS = (
    '/home/tnjn.com/templates/'
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    )

INSTALLED_APPS = (
    'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'tnjn.newssite',
    'tnjn.staff',
    'tnjn.courses',
    'tnjn.media',
    'tnjn.advertising'
)

COUNT = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),)