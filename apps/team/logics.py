# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.team.models import Team,Player,TeamProfile,PlayerProfile
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics

TEAM_DATA = {
    'name':'',
    'point':0,  #  得分
    'shot':{
        'in':0,
        'all':0,
        'rate':0
    },  # 投篮
    'three':{
        'in':0,
        'all':0,
        'rate':0
    }, # 三分
    'free':{
        'in':0,
        'all':0,
        'rate':0
    }, # 罚球
    'rebound':0, # 篮板
    'steal':0, # 抢断
    'assist':0, # 助攻
    'turnover':0, # 失误
    'block':0, # 盖帽
    'players':[],
    'game':0,
    'win':0
}
PLAYER_DATA = {
    # 'name':'',
    'point':0,  #  得分
    'shot':{
        'in':0,
        'all':0,
        'rate':0
    },  # 投篮
    'three':{
        'in':0,
        'all':0,
        'rate':0
    },
    'free':{
        'in':0,
        'all':0,
        'rate':0
    },
    'rebound':0, # 篮板
    'steal':0, # 抢断
    'assist':0, # 助攻
    'turnover':0, # 失误
    'block':0, # 盖帽
    "doubledouble":0,
    "threedouble":0,
    'game':0,
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
        teamProfile = TeamProfile()
        teamProfile = defaultProfile(teamProfile,team.id_code)
        teamProfile.save()
        team.save()
        try:
            user.player.team = team
            user.player.save() 
            user.status = 'manager'
        except:
            pass
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
    if not oldLogo is None and oldLogo != 'teamImg.jpg':
        os.remove(os.path.join(settings.TEAM_IMG,oldLogo))
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
    user.first_name = postData['first_name']
    user.status = 'player'
    playerProfile = PlayerProfile()
    playerProfile = defaultProfile(playerProfile,player.id_code)
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
    playerProfile.save()
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

def defaultProfile(tmp,id_code):
    tmp.id_code = id_code
    tmp.point = 0
    tmp.shot_in = 0
    tmp.shot_all = 0
    tmp.shot_rate = 0
    tmp.three_in = 0
    tmp.three_all = 0
    tmp.three_rate = 0
    tmp.free_in = 0
    tmp.free_all = 0
    tmp.free_rate = 0
    tmp.rebound = 0
    tmp.steal = 0
    tmp.assist = 0
    tmp.turnover = 0
    tmp.block = 0
    tmp.win = 0
    tmp.game = 0
    tmp.doubledouble = 0
    tmp.threedouble = 0
    return tmp;

def getTeamProfile(id_code):
    profile = TeamProfile.objects.get(id_code=id_code)
    return profile

def getPlayerProfile(id_code):
    profile = PlayerProfile.objects.get(id_code=id_code)
    return profile


@transaction.atomic
def adeditPlayer(player,number,height,weight,position,school,desc):
    player.number = number
    player.height = height
    player.weight = weight
    player.position = position
    player.school = school
    player.desc = desc
    player.save()
    return True



@transaction.atomic
def adeditTeam(team,name,school,desc):
    team.name = name
    team.school = school
    team.desc = desc
    team.save()
    return True


