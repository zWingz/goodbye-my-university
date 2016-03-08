#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
用户相关urls配置
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.users.views',
    url('^register$', 'register'),
    url('^login$', 'login'),
    url('^logout$', 'logout'),
    url('^usercenter$', 'usercenter'),
    url('^updateImage$', 'updateImage'),
    url('^editUserInfo$', 'editUserInfo'),
    url('^changePwd$', 'changePwd'),
    
)
