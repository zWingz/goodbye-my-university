#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Youmi
#
# @author liangmingjun@youmi.net
#
SITE_ID = 1
DEBUG = True
DEV_MODE = True
TEMPLATE_DEBUG = DEBUG
OAUTH_ENABLED = False


LOG_DIR = "/home/zwing/sites/web"
# 日志配置
# @See http://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
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
        },
        'login': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/login.log' % LOG_DIR,
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/default.log' % LOG_DIR,
        },
        'errors': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/errors.log' % LOG_DIR ,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
            'formatter': 'verbose',
        },
        'login': {
            'handlers': ['login'],
            'level': 'DEBUG',
            'propagate': True,
            'formatter': 'simple',
        },
        'errors': {
            'handlers': ['errors'],
            'level': 'INFO',
            'propagate': True,
            'formatter': 'verbose',
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'OPTIONS': {
            'DB': 3,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            }
        },
    },
}

MANAGERS = (
    ('zwing', 'zwing@z.com'),
    # ('Your Name', 'your_email@example.com'),
)

ADMIN_DATABASE = "default"

READ_FROM_SLAVE = True

CONN_MAX_AGE = 12 * 60 * 60  # 12 hour

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webbasketball',
        'USER': 'ubuntu',
        'PASSWORD': '75906116',
        # 'HOST': '192.168.201.67',
        'HOST': '10.173.160.107',
        'PORT': '3306',
    },
}

SESSION_COOKIE_DOMAIN = "192.168.56.101"

BASE_HOST = '192.168.56.101'

#STATIC_FILE_URL = 'http://127.0.0.1:8000'
STATIC_FILE_URL = 'http://192.168.56.101:8008'

# API 签名的key value
API_SECRET_MAP = {
    'local_test': '123456',
}

ALLOWED_HOSTS = [
    '127.0.0.1',
    '192.168.56.101',
    #'172.16.2.26',
    'localhost',
    "*"
]

# 允许跨域的host url
API_ALLOWED_ACCESS_HOSTS = [
    'http://192.168.56.101',
#    'http://172.16.2.22'
"*",
]

ALLOW_IP = [
    '127.0.0.1',
    #'172.16.2.22',
    '192.168.56.101',
    "*",
]

INTERNAL_IPS = [
    '127.0.0.1',
    #'172.16.2.22',
    "*",
]

# 加载到request 的通用配置
COMMON_CONFIG = {
    'CDN_VER': '20140320',
    'STATIC_FILE_URL': STATIC_FILE_URL,
}

# 配合 CommonGetParamsMiddleware使用
COMMON_GET_PARAMS = {
    # "chn_id": None,
    # "svr_id": None,
    # "start_date": None,
    # "end_date": None,
    # "date": None,
}
