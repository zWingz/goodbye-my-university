from django.shortcuts import render,redirect
import json, os, datetime,random
import copy
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import apps.game.logics as Logics
from apps.game.models import Game,PlayerGameProfile,TeamGameProfile
from apps.team.models import Team,TeamProfile,Player,PlayerProfile
from utils.Decorator.decorator import post_required,admin_required
from django.contrib.auth.decorators import login_required
from django.db.models import F,Q
# Create your views here.


def getGame(request):
    id_code = request.GET['id_code']
    game = Game.objects.get(id_code = id_code)
    team_one = game.team_one
    team_two = game.team_two
    try:
        game_profile = TeamGameProfile.objects.filter(game_id_code=id_code)
    except TeamGameProfile.DoesNotExist:
        game_profile = None
    return render(request,"game/detail.html",{"game":game,"game_profile":game_profile})


# location = ["loc_a","loc_b","loc_c","loc_d","loc_e"]


# 新建赛程
@login_required
@post_required
@admin_required
def createFixtures(request):
    teams = Team.objects.filter(status=1)
    fixtures = json.loads(request.POST['fixtures'])
    location = fixtures['location']
    fixtures = fixtures['table']
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
    choicesTeam=[]
    for time in fixtures:
        for game in time:
            if(index < teams_count):
                if len(Game.objects.filter(Q(team_one = teams[index])|Q(team_two = teams[index]),game_date=game['time']['date'])) != 0 or teams[index] in choicesTeam:
                    index = index + 1;
                    continue;
                game['location'] = location[time.index(game)%sum_location] # 顺序选取一个地点
                game['team_one'] = {"id_code":teams[index].id_code,"name":teams[index].name,"logo":teams[index].logo}
                choicesTeam.append(teams[index]) # 加入到已选队伍当中
                index = index + 1;
                next_index = random.randint(index,teams_count-1);# 在剩下队伍中找出一队
                while len(Game.objects.filter(Q(team_one = teams[next_index])|Q(team_two = teams[next_index]),game_date=game['time']['date'])) != 0:
                    next_index = random.randint(index,teams_count-1);# 找出当天没有比赛的队伍
                game['team_two'] = {"id_code":teams[next_index].id_code,"name":teams[next_index].name,"logo":teams[next_index].logo}
                choicesTeam.append(teams[next_index]) # 加入到已选队伍当中
    return HttpResponse(json.dumps(fixtures),content_type="application/json")

@login_required
@post_required
@admin_required
def saveFixtures(request):
    fixtures = json.loads(request.POST['fixtures'])
    for time in fixtures:
        if len(time) != 0:
            for game in time:
                team_one = Team.objects.get(id_code=game['team_one']['id_code'])
                team_two = Team.objects.get(id_code=game['team_two']['id_code'])
                time = game['time']['time']
                date = game['time']['date']
                Logics.saveGame(team_one,team_two,date,time,game['location'])
    response_data={}
    response_data['message'] = '赛程保存成功'
    response_data['success'] = 1
    return HttpResponse(json.dumps(response_data),content_type="application/json")

def getFixtures(request):
    if request.method == 'POST':
        weeknum = request.POST['weeknum']
        print(weeknum)
        games = Game.objects.filter(weeknum=weeknum).order_by("game_date","game_time")
        response_data = {}
        response_data['success'] = 1
        response_data['fixtures'] = toFixturesView(games)
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    elif request.method == 'GET':
        now = datetime.datetime.now()
        weeknum = request.GET.get('weeknum',str(now.isocalendar()[0])+str(now.isocalendar()[1])) 
        games = Game.objects.filter(weeknum=weeknum).order_by("game_date","game_time")
        next_weeknum = int(weeknum)+1
        next_games = Game.objects.filter(weeknum=next_weeknum)
        teamsProfile = TeamProfile.objects.all().order_by("-win_rate")[0:5]
        teams = getModelByIdCode(teamsProfile,"TeamProfile")
        pointPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-point")[0:5],"PlayerProfile")
        assistPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-assist")[0:5],"PlayerProfile")
        reboundPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-rebound")[0:5],"PlayerProfile")
        blockPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-block")[0:5],"PlayerProfile")
        stealPlayer = getModelByIdCode(PlayerProfile.objects.all().order_by("-steal")[0:5],"PlayerProfile")

        return render(request,"game/fixtures.html",{"games":games,"nextgames":next_games,
                                                                                                    "teams":teams,
                                                                                                    "pointPlayer":pointPlayer,
                                                                                                    "assistPlayer":assistPlayer,
                                                                                                    "reboundPlayer":reboundPlayer,
                                                                                                    "blockPlayer":blockPlayer,
                                                                                                    "stealPlayer":stealPlayer})

@login_required
@post_required
@admin_required
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
        if result:
            response_data['success'] = 1
            response_data['message'] = '上传成功'
            response_data['result'] = result
        else:
            response_data['success'] = 0
            response_data['message'] = '上传失败,请检查数据是否正确'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
@admin_required
def editGame(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    if id_code == "":
        game = Game()
        team_one = Team.objects.get(id_code=request.POST['team_one'])
        team_two = Team.objects.get(id_code=request.POST['team_two'])
        result = Logics.saveGame(team_one,team_two,request.POST['game-date'],request.POST['game-time'],request.POST['location'])
    else:
        game = Game.objects.get(id_code=id_code)
        result = Logics.editGame(game,request.POST['game-date'],request.POST['game-time'],request.POST['location'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '操作成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
@admin_required
def deleteGame(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    if id_code != "":
        game = Game.objects.get(id_code=id_code)
        game.delete()
        response_data['success'] = 1
        response_data['message'] = '操作成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

def toFixturesView(games):
    result = []
    for game in games:
        obj = {}
        obj['id_code'] = game.id_code
        obj['game-time'] = game.game_time
        obj['game-date'] = game.game_date
        obj['location'] = game.location
        obj['status'] = game.status
        obj['point'] = game.point
        obj['team_one'] = toTeamView(game.team_one)
        obj['team_two'] = toTeamView(game.team_two)
        result.append(obj)
    return result
    
def toTeamView(team):
    obj = {}
    obj['id_code'] = team.id_code
    obj['logo'] = team.logo
    obj['name'] = team.name
    obj['school'] = team.school
    return obj


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