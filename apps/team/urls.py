#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
球队相关urls配置
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.team.views',
    # Team
    url('^saveTeam$', 'saveTeam'),
    url('^editTeam$', 'editTeam'),
    url('^changeLogo$', 'changeLogo'),
    url('^changeTeamName$', 'changeTeamName'),
    url('^disbandTeam$', 'disbandTeam'),
    url('^getTeam$', 'getTeam'),
    url('^listTeam$', 'listTeam'),
    # Player
    url('^savePlayer$', 'savePlayer'),
    url('^editPlayer$', 'editPlayer'),
    url('^changeNum$', 'changeNum'),
    url('^joinTeam$', 'joinTeam'),
    url('^leaveTeam$', 'leaveTeam'),
    url('^getPlayer$', 'getPlayer'),
    url('^listPlayer$', 'listPlayer'),
)
