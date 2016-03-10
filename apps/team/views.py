from django.shortcuts import render
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import apps.team.logics as Logics
from apps.team.models import Team,Player
from datetime import datetime
from utils.files.logics import saveFile
from utils.Decorator.decorator import post_required
# Create your views here.

def listTeam(request):
    teamList = Team.objects.all();
    return render(request,"team/listTeam.html",{"teamList":teamList})

@post_required
def getTeamDetail(request):
    id_code = request.POST['id_code']
    team = Team.objects.get(id_code=id_code);
    players = toPlayersView(team.players.all())
    data = json.load(open(settings.TEAM_PROFILE_DIR+'/'+team.profile+'/profile','r'))
    response_data ={}
    response_data['team'] = toTeamView(team)
    response_data['players'] = players
    response_data['team_data'] = data
    return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type='application/json')

@post_required
def getPlayerDetail(request):
    id_code = request.POST['id_code']
    player = Player.objects.get(id_code=id_code);
    # data = json.load(open(settings.PLAYER_PROFILE_DIR+'/'+player.profile,'r'))
    response_data ={}
    response_data['players'] = toPlayersView([player])
    # response_data['player_data'] = data
    return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type='application/json')


# Team do something view
@login_required
def saveTeam(request):
    if request.method == 'GET':
        return render(request,"team/createTeam.html")
    else:
        response_data = {}
        response_data['success'] = 0
        response_data['message'] = '保存失败'
        result = Logics.saveTeam(request.user,request.POST)
        if result :
            response_data['success'] = 1
            response_data['message'] = '保存成功'
        return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
def editTeam(request):
    if request.method == 'GET':
        return render(request,"team/editTeam.html")
    else:
        response_data = {}
        response_data['success'] = 0
        response_data['message'] = '保存失败'
        result = Logics.editTeam(request.user,request.POST)
        if result:
            response_data['success'] = 1
            response_data['message'] = '保存成功'
        return HttpResponse(json.dumps(response_data),content_type="application/json")



@login_required
@post_required
def changeLogo(request):
    response_data = {}
    team = Team.objects.get(manager=request.user,status=1)
    if team is None:
        response_data['success'] = 0
        response_data['message'] = '无权修改'
    else:
        upfile = request.FILES['file']
        fileInfo = saveFile(upfile,os.path.join(settings.UPLOADED_DIR))
        result = Logics.changeLogo(team,fileInfo['fileUName'])
        if result:
            response_data['success'] = 1
            response_data['message'] = '修改成功'
            response_data['fileInfo']={
                                                    "filename":fileInfo['fileName'],
                                                    "url":"/static/upload/" + fileInfo['fileUName'],
                                                    "uname":fileInfo['fileUName']
                                                        };
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
def changeTeamName(request):
    response_data = {}
    team = Team.objects.get(manager = request.user,status=1)
    if team is None:
        response_data['success'] = 0
        response_data['message'] = '无权修改'
    else:
        result = Logics.changeTeamName(team,requset.POST['name'])
        if result:
            response_data['success'] = 1
            response_data['message'] = '修改成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
def disbandTeam(request):
    response_data = {}
    team = Team.objects.get(manager = request.user,status=1)
    if team is None:
        response_data['success'] = 0
        response_data['message'] = '无权修改'
    else:
        result = Logics.disbandTeam(team)
        if result:
            response_data['success'] = 1
            response_data['message'] = '修改成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")


# player do something
@login_required
def savePlayer(request):
    if request.method == 'GET':
        return render(request,"team/createPlayer.html")
    else:
        response_data = {}
        response_data["success"] = 0
        response_data["message"] = '保存失败'
        result = Logics.savePlayer(request.user,request.POST)
        if result:
            response_data["success"] = 1
            response_data["message"] = '保存成功'
        return HttpResponse(json.dumps(response_data),content_type="application/json")

# player do something
@login_required
def editPlayer(request):
    if request.method == 'GET':
        return render(request,"team/createPlayer.html")
    else:
        response_data = {}
        response_data["success"] = 0
        response_data["message"] = '保存失败'
        result = Logics.editPlayer(request.user,request.POST)
        if result:
            response_data["success"] = 1
            response_data["message"] = '保存成功'
        return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
def changeNumAndPos(request):
    response_data = {}
    team = Team.objects.get(manager=request.user,status=1)
    player = Player.objects.get(id_code=request.POST['id_code'])
    if player is None or player.team != team:
        response_data['success'] = 0
        response_data['message'] = '修改失败'
    else:
        team_players = team.players.all()
        nums = [x.number for x in team_players]
        print(nums)
        if request.POST['number'] in nums:
            response_data['success'] = 0
            response_data['message'] = '号码已存在'
        else:
            result = Logics.changeNumAndPos(player,request.POST['number'],request.POST['position'])
            if result :
                response_data['success'] = 1
                response_data['message'] = '修改成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")


@login_required
@post_required
def joinTeam(request):
    response_data = {}
    player = Player.objects.get(user=request.user)
    team = Team.objects.get(id_code=request.POST['id_code'])
    team_players = team.players_set.all()
    nums = [x.number for x in players]
    if request.POST['number'] in nums:
        response_data.success = 0
        response_data.message = '号码已存在'
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    result = Logics.joinTeam(player,team,request.POST['number'])
    if result:
        response_data.success = 1
        response_data.message = '保存成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")


@login_required
@post_required
def leaveTeam(request):
    response_data = {}
    player = Player.objects.get(user=request.user,status=1)
    if player is None:
        response_data['success'] = 0
        response_data['message'] = '退出失败'
    else:
        result = Logics.leaveTeam(player)
        if result:
            response_data.success = 1
            response_data.message = '保存成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

# get somthing
@login_required
def getMyTeam(request):
    user = request.user
    team = Team.objects.get(manager=user,status=1)
    identity = 'normal'
    if team is None:
        player = Player.objects.get(user=user,status=1)
        if team is not None:
            team = player.team
            identity = 'player'
    else:
        identity = 'manager'
    return render(request,"team/info",{team:team,identity:identity})

def getTeam(request):
    team = Team.objects.get(name=request.GET['name'])
    return render(request,"team/info",{team:team})


@login_required
def getMyPlayer(request):
    user = request.user
    player = Player.objects.get(user=user,status=1)
    return render(request,"team/info",{player:player,isPlayer:True})

def getPlayer(request):
    player = Player.objects.get(user_username=request.GET['name'])
    return render(request,"team/player",{player:player})


# list something
# def listTeam(request):
#     id_code = request.POST['id_code']
#     name = request.POST['name']
#     status = request.POST['status']
#     teams = Team.objects.filter(id_code=id_code,name=name,status=status)
#     return render(request,"team/listteam",{teams:teams})

def listPlayer(request):
    team_id = request.GET['id_code']
    team = Team.objects.get(id_code=id_code,status=1)
    players = team.players_set.all()
    return render(request,"team/listplayers",{players:players})

def toPlayersView(players):
    result = []
    for player in players:
        obj = {}
        obj['id_code'] = player.id_code
        obj['name'] = player.user.first_name
        obj['nickname'] = player.user.last_name
        obj['phone'] = player.user.phone
        obj['qq'] = player.user.qq
        obj['img_path'] = player.user.img_path
        obj['position'] = player.position
        obj['height'] = player.height
        obj['school'] = player.school
        obj['weight'] = player.weight
        obj['number'] = player.number
        obj['create_time'] = player.create_time
        obj['desc'] = player.desc
        result.append(obj)
    return result

def toTeamView(team):
    obj = {}
    obj['id_code'] = team.id_code
    obj['logo'] = team.logo
    obj['name'] = team.name
    obj['manager'] = team.manager.first_name
    obj['school'] = team.school
    obj['create_time'] = team.create_time
    obj['desc'] = team.desc
    return obj

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)