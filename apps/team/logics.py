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
from utils.files.logics as fileLogics

# Team do something
@transaction.atomic
def saveTeam(user,postData):
    teams = Team.objects.filter(user=user,status=1)
    if teams.length > 0:
        team = teams[0]
    else:
        team = Team()
        team.id_code = fileLogics.getTeamIdCode()
        team.manager = user
        user.status = 'manager'
        team.name = postData['name']
        profile = postData['name']
        logo = postData['logo']
    school = postData['school']
    desc = postData['desc']
    os.mkdir(os.path.join(setting.TEAM_PROFILE_DIR,team.name))
    with open(settings.TEAM_PROFILE_DIR+"/"+team.name+"/profile","wb+") as fp:
        fp.write("")
    team.save()
    user.save()
    fileLogics.setTeamIdCode(team.id_code+1)
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
def savePlayer(user,postData):
    if user.player is None
        player = Player()
        player.id_code = fileLogics.getPlayerIdCode()
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
    fileLogics.setPlayerIdCode(player.id_code+1)
    return True

def changeNum(player,number):
    player.number = number
    player.save()
    return True

def joinTeam(player,team,number):
    player.team = team
    player.number = number
    player.save()
    return True

def leaveTeam(player):
    player.team = null
    player.number = null
    player.save();
    return True


# # get somthing


# def getPlayer(username,status=1):
#     player = Player.objects.get(user_username=username,status=status)
#     return player

# def get_user(username):
#     return User.objects.get(username=username)

# def get_team(username,status=1):
#     team = Team.objects.get(user_username=username,status=status)
#     if team is None
#         team = Player.objects.get(user_username=username,status=status).team
#     if team is None
#         team = {}
#     return team

# #  list something
# def listTeamPlayers(teamname,status=1):
#     players = Team.objects.get(name=teamname,status=status).players_set.all()
#     return players

# def listTeam(status=1):
#     teams = Team.objects.filter(status=status)
#     return teams

# def listTeamNum(teamname,status=1):
#     players = listTeamPlayers(teamname,status)
#     nums = [x.number for x in players]
#     return nums    
