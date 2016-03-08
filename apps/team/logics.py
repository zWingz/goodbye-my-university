# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.team.models import Team,Player
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics

# Team do something
@transaction.atomic
def saveTeam(user,postData):
    teams = Team.objects.filter(user=user,status=1)
    if teams.length > 0:
        team = teams[0]
    else:
        team = Team()
        team.id_code = fileLogics.getIdCode("TEAM")
        team.manager = user
        user.status = 'manager'
        team.name = postData['name']
        profile = postData['name']
        logo = postData['logo']
    school = postData['school']
    desc = postData['desc']
    os.mkdir(os.path.join(settings.TEAM_PROFILE_DIR,team.name))
    with open(settings.TEAM_PROFILE_DIR+"/"+team.name+"/profile","wb+") as fp:
        fp.write("")
    team.save()
    user.save()
    fileLogics.setIdCode("TEAM",int(team.id_code)+1)
    return True;

@transaction.atomic
def changeLogo(team,logo):
    oldLogo = team.logo
    os.remove(os.path.join(settings.UPLOADED_DIR,oldLogo))
    team.logo = logo
    team.save()
    return True

@transaction.atomic
def changeTeamName(team,name):
    team.name = name
    oldProfile = team.profile
    team.profile = name
    os.rename(os.path.join(settings.TEAM_PROFILE_DIR,oldProfile),os.path.join(setting.TEAM_PROFILE_DIR,name))
    team.save()
    return True

@transaction.atomic
def disbandTeam(team):
    # team = get_team(username)
    team.status = 0
    team.save()
    return True

# Player do something
@transaction.atomic
def savePlayer(user,postData):
    if user.player is None:
        player = Player()
        player.id_code = fileLogics.getIdCode("PLAYER")
        player.user = user
        user.status = 'player'
        with open(settings.PLAYER_PROFILE_DIR+"/"+id_code,"wb+") as fp:
            fp.write("")
        player.profile = id_code
    else:
        player = user.player
    player.position = postData['position']
    player.desc = postData['desc']
    player.save()
    user.save()
    fileLogics.setIdCode("PLAYER",int(player.id_code)+1)
    return True

@transaction.atomic
def changeNum(player,number):
    player.number = number
    player.save()
    return True

@transaction.atomic
def joinTeam(player,team,number):
    player.team = team
    player.number = number
    player.save()
    return True

@transaction.atomic
def leaveTeam(player):
    player.team = null
    player.number = null
    player.save();
    return True

