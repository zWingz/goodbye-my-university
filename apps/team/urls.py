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
    url('^teamDetail$', 'teamDetail'),

    url('^listPlayer$', 'listPlayer'),
    # Team
    url('^saveTeam$', 'saveTeam'),
    url('^editTeam$', 'editTeam'),
    url('^changeLogo$', 'changeLogo'),
    url('^changeTeamName$', 'changeTeamName'),
    url('^disbandTeam$', 'disbandTeam'),
    # Player
    # getPlayerDetail
    url('^playerDetail$', 'playerDetail'),
    url('^savePlayer$', 'savePlayer'),
    url('^editPlayer$', 'editPlayer'),
    url('^changeNumAndPos$', 'changeNumAndPos'),
    url('^agreeApplyJoinTeam$', 'agreeApplyJoinTeam'),
    
    url('^agreeInviteJoinTeam$', 'agreeInviteJoinTeam'),
    url('^leaveTeam$', 'leaveTeam'),

    url('^checkNum$', 'checkNum'),

    # 同意比赛
    url('^agreeInviteGame$', 'agreeInviteGame'),
)
