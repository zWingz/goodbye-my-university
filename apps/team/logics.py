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

TEAM_DATA = {
    'name':'',
    'point':'0',  #  得分
    'shot':'0/0',  # 投篮
    'three':'0/0', #三分
    'rebound':'0', # 篮板
    'steal':'0', # 抢断
    'assist':'0', # 助攻
    'turnover':'0', # 失误
    'block':'0', # 盖帽
    'players':[],
    'game':"0",
    "win":"0"
}
PLAYER_DATA = {
    # 'name':'',
    'point':'0',  #  得分
    'assist':'0', # 助攻
    'shot':'0/0',  # 投篮
    'three':'0/0', #三分
    'rebound':'0', # 篮板
    'steal':'0', # 抢断
    "free":'0/0', #  罚球
    'turnover':'0', # 失误
    'block':'0', # 盖帽
    "doubledouble":'0',
    "threedouble":'0',
    'game':"0",
}
# Team do something
@transaction.atomic
def saveTeam(user,postData):
    teams = Team.objects.filter(manager=user,status=1)
    if len(teams) > 0:
        return False
    else:
        team = Team()
        team.id_code = fileLogics.getIdCode("TEAM")
        team.manager = user
        user.status = 'manager'
        team.name = postData['name']
        team.profile = team.id_code
        # logo = postData['logo']
        team.school = postData['school']
        team.desc = postData['desc']
        os.mkdir(os.path.join(settings.TEAM_PROFILE_DIR,team.id_code))
        with open(settings.TEAM_PROFILE_DIR+"/"+team.id_code+"/profile","w+") as fp:
            fp.write(json.dumps(TEAM_DATA))
        team.save()
        if not user.player is None:
            user.player.team = team
            user.player.save() 
        user.save()
        fileLogics.setIdCode("TEAM",int(team.id_code)+1)
        return True;

@transaction.atomic
def editTeam(user,postData):
    teams = Team.objects.filter(manager=user,status=1)
    if len(teams) == 0:
        return False
    else:
        team = teams[0]
        team.name = postData['name']
        team.school = postData['school']
        team.desc = postData['desc']
        team.save()
        return True;


@transaction.atomic
def changeLogo(team,logo):
    oldLogo = team.logo
    if not oldLogo is None:
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
    player = Player()
    player.id_code = fileLogics.getIdCode("PLAYER")
    player.user = user
    user.status = 'player'
    with open(settings.PLAYER_PROFILE_DIR+"/"+player.id_code,"w+") as fp:
        fp.write(json.dumps(PLAYER_DATA))
    player.profile = player.id_code
    height = postData['height']
    if height[-2:] != 'cm':
        height = height + 'cm'
    weight = postData['weight']
    if weight[-2:] != 'kg':
        weight = weight + 'kg'
    player.height = height
    player.weight = weight
    player.position = postData['position']
    player.desc = postData['desc']
    player.save()
    user.save()
    fileLogics.setIdCode("PLAYER",int(player.id_code)+1)
    return True

@transaction.atomic
def editPlayer(user,postData):
    player = user.player
    # with open(settings.PLAYER_PROFILE_DIR+"/"+player.id_code,"w+") as fp:
    #     fp.write("")
    height = postData['height']
    if height[-2:] != 'cm':
        height = height + 'cm'
    weight = postData['weight']
    if weight[-2:] != 'kg':
        weight = weight + 'kg'
    player.height = height
    player.weight = weight
    # if player.team is None:
        # player.position = postData['position']
    player.desc = postData['desc']
    player.school = postData['school']
    player.save()
    return True


@transaction.atomic
def changeNumAndPos(player,number,position):
    player.number = number
    player.position = position
    player.save()
    return True

@transaction.atomic
def joinTeam(player,team,number,position):
    player.team = team
    player.number = number
    player.position = position
    player.save()
    return True



@transaction.atomic
def leaveTeam(player):
    player.team = null
    player.number = null
    player.save();
    return True



def checkNum(team,num):
    team_players = team.players.all()
    nums = [x.number for x in team_players]
    if num in nums:
        return True;
    else:
        return False;