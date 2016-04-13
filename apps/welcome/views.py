from django.shortcuts import render
from django.http import HttpResponse
import json,datetime
from apps.message.models import News
from apps.game.models import Game,PlayerGameProfile,TeamGameProfile
from apps.team.models import Team,TeamProfile,Player,PlayerProfile
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from operator import attrgetter
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
    querySet = PlayerProfile.objects.all()
    pointPlayer = getModelByIdCode(sorted(querySet,key=lambda s:s.avg_point,reverse=True)[0:5],"PlayerProfile","point")
    assistPlayer = getModelByIdCode(sorted(querySet,key=lambda s:s.avg_assist,reverse=True)[0:5],"PlayerProfile","assist")
    reboundPlayer = getModelByIdCode(sorted(querySet,key=lambda s:s.avg_rebound,reverse=True)[0:5],"PlayerProfile","rebound")
    blockPlayer = getModelByIdCode(sorted(querySet,key=lambda s:s.avg_block,reverse=True)[0:5],"PlayerProfile","block")
    stealPlayer = getModelByIdCode(sorted(querySet,key=lambda s:s.avg_steal,reverse=True)[0:5],"PlayerProfile","steal")
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



def getModelByIdCode(objlist,modelType,sortType=None):
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
                    setattr(player,sortType,getattr(each,sortType)/each.game)
                    result.append(player)
    return result