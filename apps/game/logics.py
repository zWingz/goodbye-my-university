# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.game.models import Game
from apps.team.models import Team
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics
import copy 
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
def saveGame(team_one,team_two,game_time,location):
    game = Game()
    game.team_one = team_one
    game.team_two = team_two
    game.game_time = game_time
    game.location = location
    game.weeknum = str(game_time.isocalendar()[0])+str(game_time.isocalendar()[1])
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

