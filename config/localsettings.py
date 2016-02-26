# 本地配置文件
import os
# 数据库
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webbasketball',
        'USER': 'zwing',
        'PASSWORD': '75906116',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}


ROOT_URLCONF = 'config.urls'


ALLOWED_HOSTS = [
    '127.0.0.1', ]
