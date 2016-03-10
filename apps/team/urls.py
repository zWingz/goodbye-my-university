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
    url('^listTeam$', 'listTeam'),
    url('^getTeamDetail$', 'getTeamDetail'),
    # Team
    url('^saveTeam$', 'saveTeam'),
    url('^editTeam$', 'editTeam'),
    url('^changeLogo$', 'changeLogo'),
    url('^changeTeamName$', 'changeTeamName'),
    url('^disbandTeam$', 'disbandTeam'),
    url('^getTeam$', 'getTeam'),
    url('^getMyTeam$', 'getMyTeam'),
    # Player
    # getPlayerDetail
    url('^getPlayerDetail$', 'getPlayerDetail'),
    url('^savePlayer$', 'savePlayer'),
    url('^editPlayer$', 'editPlayer'),
    url('^changeNumAndPos$', 'changeNumAndPos'),
    url('^joinTeam$', 'joinTeam'),
    url('^leaveTeam$', 'leaveTeam'),
    url('^getPlayer$', 'getPlayer'),
    url('^listPlayer$', 'listPlayer'),
)
