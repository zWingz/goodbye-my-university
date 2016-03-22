#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
比赛相关urls配置
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.admin.views',
    url(r'^$', 'admin_index'),
    url(r'^login$', 'loginAdmin'),
    url('^fixtures$', 'getFixtures'),
    # url('^saveFixtures$', 'saveFixtures'),
    # url('^fixtures$', 'getFixtures'),
)
