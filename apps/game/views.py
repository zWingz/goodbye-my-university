from django.shortcuts import render,redirect
import json, os, time
import copy
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import apps.game.logics as Logics
from apps.team.models import Team
from utils.Decorator.decorator import post_required
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
@post_required
def saveGame(request):
    response_data = {}
    result = Logics.saveGame(request.POST)
    return redirect(getGame,game=request.POST['game'])

def getGame(request):
    id_code = request.GET['game']
    game = Game.objects.get(id_code = id_code)
    team_one = game.team_one
    team_two = game.team_two
    path = open(os.path.join(settings.GAME_PROFILE_DIR,game.profile),'r')
    game_data = json.load(path)
    return render(request,"game/detial",{team_one:team_one,team_two:team_two,game_data:game_data})

location = ["loc_a","loc_b","loc_c","loc_d","loc_e"]

GAME_TIME = [
    [{"time":"2016-03-14 18:00","location":""}],
    [],
    [{"time":"2016-03-16 18:30","location":""}],
    [],
    [{"time":"2016-03-18 18:30","location":""}],
    [{"time":"2016-03-19 10:30","location":""},{"time":"2016-03-19 14:30","location":""},{"time":"2016-03-19 16:30","location":""}],
    [{"time":"2016-03-20 10:30","location":""},{"time":"2016-03-20 14:30","location":""},{"time":"2016-03-20 16:30","location":""}]
];

# 新建赛程
# @post_required
def createFixtures(request):
    teams = Team.objects.filter(status=1)
    game_time = copy.deepcopy(GAME_TIME)
    for team in teams:
        game = json.load(open(settings.TEAM_PROFILE_DIR+"/"+team.profile+"/profile","r"))["game"]
        team.game = game
    teams = list(teams)
    teams_count = len(teams)
    sorted(teams,key=lambda s: s.game)
    sum_location = len(location)
    index = 0;
    for time in game_time:
        for game in time:
            if(teams_count < index + 2):
                break;
            game['location'] = location[time.index(game)%sum_location]
            game['team_one'] = teams[index].name
            index = index + 1;
            game['team_two'] = teams[index].name
            index = index + 1;
    return HttpResponse(json.dumps(game_time),content_type="application/json")


def saveFixtures(request):
    game_time = request.POST['game_time']
    for time in game_time:
        if len(time) != 0:
            for game in time:
                team_one = Team.objects.get(name=game.team_one)
                team_two = Team.objects.get(name=game.team_two)
                time = datetime.datetime.strptime(game.time, "%Y-%m-%d %H:%M:%S")
                Logics.saveGame(team_one,team_two,time,game.location)
    response_data={}
    response_data['success'] = 1
    return HttpResponse(json.dumps(game_time),content_type="application/json")


# def getFixtures(request):
    