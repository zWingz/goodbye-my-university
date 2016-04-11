from django.shortcuts import render
from django.http import HttpResponse
import json,datetime
from apps.message.models import News
from apps.game.models import Game,PlayerGameProfile,TeamGameProfile
from apps.team.models import Team,TeamProfile,Player,PlayerProfile
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
# Create your views here.
def welcome(request):
    news = News.objects.all().order_by("-create_time")[0:5]
    today = datetime.date.today()
    next_day = today+ datetime.timedelta(days=1)
    prev_day = today -  datetime.timedelta(days=1)
    today_game = Game.objects.filter(game_date=today.strftime("%Y-%m-%d")).order_by("game_time")
    next_day_game = Game.objects.filter(game_date=next_day.strftime("%Y-%m-%d")).order_by("game_time")
    prev_day_game = Game.objects.filter(game_date=prev_day.strftime("%Y-%m-%d")).order_by("game_time")

    teamsProfile = TeamProfile.objects.all().order_by("-win_rate")[0:5]
    teams = getModelByIdCode(teamsProfile,"TeamProfile")
    pointPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-point")[0:5],"PlayerProfile")
    assistPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-assist")[0:5],"PlayerProfile")
    reboundPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-rebound")[0:5],"PlayerProfile")
    blockPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-block")[0:5],"PlayerProfile")
    stealPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-steal")[0:5],"PlayerProfile")
    return render(request,"index.html",{
            "todayGame":today_game,
            "nextDayGame":next_day_game,
            "prevDayGame":prev_day_game,
            "news":news,
            "teams":teams,
            "pointPlayer":pointPlayer,
            "assistPlayer":assistPlayer,
            "reboundPlayer":reboundPlayer,
            "blockPlayer":blockPlayer,
            "stealPlayer":stealPlayer
        })



def getModelByIdCode(objlist,modelType):
    result = []
    if len(objlist)==0:
        return result
    if modelType == 'TeamProfile':
        for each in objlist:
            team = Team.objects.get(id_code=each.id_code)
            team.win_rate = each.win_rate
            team.game = each.game
            result.append(team)
    elif modelType == 'PlayerProfile':
        for each in objlist:
            player = Player.objects.get(id_code=each.id_code)
            if each.game != 0 :
                player.point = each.point/each.game
                player.rebound = each.rebound/each.game
                player.assist = each.assist/each.game
                player.steal = each.steal/each.game
                player.block = each.block/each.game
                result.append(player)
            player.game = each.game
    return result