#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# Django settings for game_data project.
import os

BASEDIR = os.getcwd()
VENDORS_ROOT = os.path.join(BASEDIR, "vendors")
UPLOADED_DIR = os.path.join(BASEDIR, "static/upload")
TEAM_PROFILE_DIR = os.path.join(BASEDIR, "static/files/teamProfiles")
PLAYER_PROFILE_DIR = os.path.join(BASEDIR, "static/files/playerProfiles")

# ini 文件Dir
ID_CODE_INI = os.path.join(BASEDIR, "config/id_code.ini")

ADMINS = (
    ('zwing', 'zwing@z.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Chongqing'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-hans'

# SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASEDIR, "static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASEDIR, "static"),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'change_this_please_dshdfgh2Q#@DFG@#$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    # 'apps.common.views.getDepart',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',

    # user agent 第三方库
    # @see https://github.com/selwin/django-user_agents
    # 'django_user_agents.middleware.UserAgentMiddleware',

    # 自定义中间件
    # 'utils.cfg.middleware.OuwanCommonConfigMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
)

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

ROOT_URLCONF = 'config.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATE_DIRS = (
    #os.path.join(BASEDIR, "templates/custom"),
    os.path.join(BASEDIR, "templates"),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    #'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',

    # user agent 第三方库
    # @see https://github.com/selwin/django-user_agents
    #'debug_toolbar',
    # 'django_user_agents',

    # 'apps.authen',
    'apps.welcome',
    'apps.users',
    'apps.team',
    'apps.usual',
    'apps.message'
)

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3 * 24 * 60 * 60
# SESSION_COOKIE_DOMAIN = "game.dev.youmi.net"

# 默认分页长度
PAGELEN = 10

# 默认登陆页面
LOGIN_URL = '/auth/login/'

# 登陆成功后跳转的页面
LOGIN_REDIRECT_URL = "/"

DATABASE_ROUTERS = [
    'utils.db.router.DBRouter'
]

EMAIL_HOST_USER = 'afs@youmi.net'

DEBUG = True

# localsettings 放到最后，以覆盖默认配置
from config.localsettings import *

