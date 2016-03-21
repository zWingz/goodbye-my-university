from django.shortcuts import render,redirect
import json, os, datetime
import copy
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import apps.game.logics as Logics
from apps.game.models import Game
from apps.team.models import Team,TeamProfile
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
    fixtures = json.loads(request.POST['fixtures'])
    response_data = []
    for team in teams:
        team_profile = TeamProfile.objects.get(id_code=team.id_code)
        game = team_profile.game
        team.game = game
    teams = list(teams)
    teams_count = len(teams)
    sorted(teams,key=lambda s: s.game)
    sum_location = len(location)
    index = 0;
    for time in fixtures:
        for game in time:
            if(teams_count < index + 2):
                break;
            game['location'] = location[time.index(game)%sum_location]
            game['team_one'] = {"id_code":teams[index].id_code,"name":teams[index].name,"logo":teams[index].logo}
            index = index + 1;
            game['team_two'] = {"id_code":teams[index].id_code,"name":teams[index].name,"logo":teams[index].logo}
            index = index + 1;
    return HttpResponse(json.dumps(fixtures),content_type="application/json")


def saveFixtures(request):
    fixtures = json.loads(request.POST['fixtures'])
    print(fixtures)
    index = 0
    for time in fixtures:
        if len(time) != 0:
            for game in time:
                team_one = Team.objects.get(id_code=game['team_one']['id_code'])
                team_two = Team.objects.get(id_code=game['team_two']['id_code'])
                time = game['time']['time']
                date = game['time']['date']
                Logics.saveGame(team_one,team_two,date,time,game['location'],index)
        index = index + 1
    response_data={}
    response_data['success'] = 1
    return HttpResponse(json.dumps(response_data),content_type="application/json")

def getFixtures(request):
    if request.method == 'POST':
        weeknum = request.POST['weeknum']
        games = Game.objects.filter(weeknum=weeknum)
        response_data = {}
        response_data['success'] = 1
        response_data['fixtures'] = toFixturesView(games)
        return HttpResponse(json.dumps(game_time),content_type="application/json")
    elif request.method == 'GET':
        now = datetime.datetime.now()
        weeknum = request.GET.get('weeknum',str(now.isocalendar()[0])+str(now.isocalendar()[1])) 
        games = Game.objects.filter(weeknum=weeknum)

        next_weeknum = int(weeknum)+1
        next_games = Game.objects.filter(weeknum=next_weeknum)
        return render(request,"game/fixtures.html",{"games":games,"nextgames":next_games})

@post_required
def uploadData(request):
    response_data = {}
    game = Game.objects.get(id_code=request.POST['id_code'])
    if game is None:
        response_data['success'] = 0
        response_data['message'] = '无权修改'
    else:
        upfile = request.FILES['file']
        extention =  upfile.name[upfile.name.rfind('.'):]
        fileName = request.POST['id_code'] + extention
        with open(settings.GAME_PROFILE_DIR+"/"+fileName, 'wb+') as dest:
            for chunk in upfile.chunks():
                dest.write(chunk)
        result = Logics.parseDatFromExcel(fileName)
        result = Logics.saveData(game,result)
        response_data['success'] = 1
        response_data['message'] = '修改成功'
        response_data['result'] = result
    return HttpResponse(json.dumps(response_data),content_type="application/json")



def toFixturesView(games):
    result = [[],[],[],[],[],[],[]]
    for game in games:
        obj = {}
        obj['game-time'] = game.game_time
        obj['location'] = game.location
        obj['status'] = game.status
        obj['point'] = game.point
        obj['team_one'] = toTeamView(game.team_one)
        obj['team_two'] = toTeamView(game.team_two)
        result[game.week_index].append(obj)
    return result
    
def toTeamView(team):
    obj = {}
    obj['id_code'] = team.id_code
    obj['logo'] = team.logo
    obj['name'] = team.name
    obj['school'] = team.school
    return obj