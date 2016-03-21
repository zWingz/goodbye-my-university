# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.game.models import Game,GameProfile,PlayerGameProfile,TeamGameProfile
from apps.team.models import Team,Player,TeamProfile,PlayerProfile
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics
import copy 
import xlrd
RESULT = {
    'win':{},
    'lost':{}
}
TEAM_DATA = {
    'name':'',
    'point':'',  #  得分
    'shot':'',  # 投篮
    'three':'', #三分
    'rebound':'', # 篮板
    'free':'', # 罚球
    'steal':'', # 抢断
    'assist':'', # 助攻
    'turnover':'', # 失误
    'block':'', # 盖帽
    'players':[]
}
PLAYER_DATA = {
    'name':'',
    'point':'',  #  得分
    'shot':'',  # 投篮
    'three':'', #三分
    'rebound':'', # 篮板
    'free':'', # 罚球
    'steal':'', # 抢断
    'assist':'', # 助攻
    'turnover':'', # 失误
    'block':'', # 盖帽
    'foul':'' # 犯规
}
@transaction.atomic
def saveGame(team_one,team_two,date,time,location,week_index):
    game = Game()
    game.team_one = team_one
    game.team_two = team_two
    game.game_date = date
    game.game_time = time
    game.location = location
    num = datetime.datetime.strptime(date, "%Y-%m-%d")
    game.weeknum = str(num.isocalendar()[0])+str(num.isocalendar()[1])
    game.week_index = week_index
    game.save()
    return True

@transaction.atomic
def saveDetailData(postData):
    result = {}
    id_code = postData['game']
    game = Game.objects.get(id_code=id_code)
    # win =  copy.deepcopy(TEAM_DATA)
    # lost = copy.deepcopy(TEAM_DATA)
    result = postData['game_data']
    path = os.path.join(settings.GAME_PROFILE_DIR,game_time.strftime('%Y-%m-%d'))
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path,game.id_code),"wb+") as fp:
        fp.write(json.dumps(result))
    game.data_profile = str(os.path.join(game_time.strftime('%Y-%m-%d'),game.id_code))
    game.save()
    return True


def saveData(game,data):
    team_one = None
    team_two = None
    team_one_profile = None
    team_two_profile = None
    team_one_gprofile = None
    team_two_gprofile = None
    point = ""
    for each in data:
        if each['type'] == 'team':
            if str(int(each['id_code'])) == game.team_one.id_code:
                team_one = each
                team_one_gprofile = TeamGameProfile()
                team_one_gprofile.id_code = game.team_one.id_code
                saveProfile(team_one_gprofile,each)
                point = str(int(each['point']))+" - "
                team_one_profile = TeamProfile.objects.get(id_code=str(int(each['id_code'])))
                saveProfile(team_one_profile,each)
                team_one_profile.game += 1
            else:
                team_two = each
                team_two_gprofile = TeamGameProfile()
                team_two_gprofile.id_code = game.team_two.id_code
                saveProfile(team_two_gprofile,each)
                point = point + str(int(each['point']))
                team_two_profile = TeamProfile.objects.get(id_code=str(int(each['id_code'])))
                saveProfile(team_two_profile,each)
                team_two_profile.game += 1
            game.point = point
            game.status = 1
    if int(team_one['point']) > int(team_two['point']):
        team_one_profile.win += 1
    else:
        team_one_profile.win += 1
    team_one_profile.save()
    team_one_gprofile.save()
    team_two_profile.save()
    team_two_gprofile.save()
    for each in data:
        if each['type'] == 'player':
            player = Player.objects.get(id_code=str(int(each['id_code'])))
            player_game_profile = PlayerGameProfile()
            player_profile = PlayerProfile.objects.get(id_code=str(int(each['id_code'])))
            saveProfile(player_profile,each)
            saveProfile(player_game_profile,each)
            player_profile.game += 1
            if checkDoubleCount(each) >= 3:
                player_profile.threedouble +=1
            elif checkDoubleCount(each) >= 2:
                player_profile.doubledouble+=1;
            if player.team.id_code == str(int(team_one['id_code'])):
                team_one_gprofile.players.append(player_game_profile)
                player_game_profile.team_game = team_one_gprofile
            else:
                team_two_gprofile.players.append(player_game_profile)
                player_game_profile.team_game = team_two_gprofile
            player_profile.save()
            player_game_profile.id_code = player.id_code
            player_game_profile.save()
    game_profile = GameProfile()
    game_profile.id_code = game.id_code
    game_profile.team_one_profile = team_one_gprofile
    game_profile.team_two_profile = team_two_gprofile

    game.save()
    game_profile.save()
    return True


def checkDoubleCount(data):
    result = 0
    if int(data['point']) > 10:
        result = result + 1;
    if int(data['rebound']) > 10:
        result = result + 1;
    if int(data['steal']) > 10:
        result = result + 1;
    if int(data['assist']) > 10:
        result = result + 1;
    if int(data['block']) > 10:
        result = result + 1;
    return result

def saveProfile(profile,data):
    profile.point = (profile.point or 0) + int(data['point'])
    profile.shot_in = (profile.shot_in or 0) + int(data['shot_in'])
    profile.shot_all = (profile.shot_all or 0) + int(data['shot_all'])
    profile.three_in = (profile.three_in or 0) + int(data['three_in'])
    profile.three_all = (profile.three_all or 0) + int(data['three_all'])
    profile.free_in = (profile.free_in or 0) + int(data['free_in'])
    profile.free_all = (profile.free_all or 0) + int(data['free_all'])
    profile.rebound = (profile.rebound or 0) + int(data['rebound'])
    profile.steal = (profile.steal or 0) + int(data['steal'])
    profile.assist = (profile.assist or 0) + int(data['point'])
    profile.turnover = (profile.turnover or 0) + int(data['turnover'])
    profile.block = (profile.block or 0) + int(data['block'])


def parseDatFromExcel(file_name):
    data = xlrd.open_workbook(os.path.join(settings.GAME_PROFILE_DIR,file_name))
    table = data.sheets()[0]   
    header = table.row_values(0)
    colLen = table.ncols
    rowLen = table.nrows
    key_map = []
    result = []
    for i in range(colLen):
        key_map.append(table.cell(0,i).value);
    for i in range(1,rowLen):
        obj = {}
        for j in range(colLen):
            obj[key_map[j]] = table.cell(i,j).value
        result.append(obj)
    return result


