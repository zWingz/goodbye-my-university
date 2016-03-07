#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
消息相关urls配置
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.message.views',
    url('^sendMsg$', 'sendMsg'),
    url('^readMsg$', 'readMsg'),
    url('^sendJoinTeamMsg$', 'sendJoinTeamMsg'),
    url('^listUnReadMsg$', 'listUnReadMsg'),
    url('^listAllMsg$', 'listAllMsg'),


)
