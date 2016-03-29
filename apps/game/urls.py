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
    'apps.game.views',
    url('^createFixtures$', 'createFixtures'),
    url('^getGame$', 'getGame'),
    url('^editGame$', 'editGame'),
    url('^deleteGame$', 'deleteGame'),
    url('^saveFixtures$', 'saveFixtures'),
    url('^fixtures$', 'getFixtures'),
    url('^uploadData$', 'uploadData'),
)
