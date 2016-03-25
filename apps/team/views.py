from django.shortcuts import render
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import apps.team.logics as Logics
import apps.message.logics as MsgLogics
from apps.team.models import Team,Player
from apps.game.models import Game
from apps.message.models import Message
import datetime
from utils.files.logics import saveFile
from utils.Decorator.decorator import post_required
from django.contrib.auth.models import User  
from django.db.models import Q
# Create your views here.

def listTeam(request):
    teamList = Team.objects.all();
    return render(request,"team/listTeam.html",{"teamList":teamList})


def listPlayer(request):
    playerList = Player.objects.all();
    return render(request,"team/listPlayer.html",{"playerList":playerList})

def teamDetail(request):
    id_code = request.REQUEST['id_code']
    team = Team.objects.get(id_code=id_code,status=1);
    players = toPlayersView(team.players.all())
    data = Logics.getTeamProfile(id_code);
    if request.method == 'GET':
        now = datetime.datetime.now()
        weeknum = str(now.isocalendar()[0])+str(now.isocalendar()[1])
        games = Game.objects.filter(Q(team_one=team)|Q(team_two=team),weeknum=weeknum)
        nextgames =  Game.objects.filter(Q(team_one=team)|Q(team_two=team),weeknum=int(weeknum)+1)
        otherTeam = list(Team.objects.all().order_by('?')[:5])
        index = otherTeam.index(team)
        del otherTeam[index]
        return render(request,"team/teamDetail.html",{"team":team,"players":players,"team_data":data,"games":games,"nextgames":nextgames,"otherTeam":otherTeam})
    else:
        response_data ={}
        response_data['team'] = toTeamView(team)
        response_data['players'] = players
        response_data['team_data'] = toTeamProfileView(data)
        return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type='application/json')

def playerDetail(request):
    id_code = request.REQUEST['id_code']
    player = Player.objects.get(id_code=id_code);
    if request.method == 'GET':
        data = Logics.getPlayerProfile(id_code)
        teammates = list(player.team.players.all())
        teammates.remove(player)
        return render(request,"team/playerDetail.html",{"player":player,"player_data":data,"teammates":teammates})
    else:
        response_data ={}
        response_data['players'] = toPlayersView([player])
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

# 改变球员号码和位置
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
        if Logics.checkNum(team,request.POST['number']):
            response_data['success'] = 0
            response_data['message'] = '号码已存在'
        else:
            result = Logics.changeNumAndPos(player,request.POST['number'],request.POST['position'])
            if result :
                response_data['success'] = 1
                response_data['message'] = '修改成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

# 同意加入申请
@login_required
@post_required
def agreeApplyJoinTeam(request):
    response_data = {}
    user = User.objects.get(id_code=request.POST['id_code'])
    player = Player.objects.get(user=user)
    msg = Message.objects.get(id_code=request.POST['msg_id_code'])
    team = request.user.team.all()[0]
    if Logics.checkNum(team,request.POST['r-number']):
        response_data['success'] = 0
        response_data['message'] = '号码已存在'
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    result = Logics.joinTeam(player,team,request.POST['r-number'],request.POST['r-position'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '保存成功'
        MsgLogics.readMsg(msg)
    return HttpResponse(json.dumps(response_data),content_type="application/json")


# 同意邀请
@login_required
@post_required
def agreeInviteJoinTeam(request):
    response_data = {}
    user = User.objects.get(id_code=request.POST['id_code'])
    team = Team.objects.get(manager=user,status=1)
    msg = Message.objects.get(id_code=request.POST['msg_id_code'])
    player = request.user.player
    if Logics.checkNum(team,request.POST['r-number']):
        response_data['success'] = 0
        response_data['message'] = '号码已存在'
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    result = Logics.joinTeam(player,team,request.POST['r-number'],request.POST['r-position'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '保存成功'
        MsgLogics.readMsg(msg)
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



def checkNum(request):
    team = Team.objects.get(id_code=request.POST['id_code'])
    if checkNum(team,request.POST['number']):
        response_data['success'] = 0
        response_data['message'] = '号码已存在'
    else:
        response_data['success'] = 1
    return HttpResponse(json.dums(response_data),content_type='application/json')



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
        data = Logics.getPlayerProfile(player.id_code)
        obj['player_data'] = toPlayerProfileView(data)
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

# 对象转字典
def toTeamProfileView(profile):
    obj={
        'point':profile.point,  #  得分
        'shot':{
            'in':profile.shot_in,
            'all':profile.shot_all,
            'rate':profile.shot_rate
        },  # 投篮
        'three':{
            'in':profile.three_in,
            'all':profile.three_all,
            'rate':profile.three_rate
        }, # 三分
        'free':{
            'in':profile.free_in,
            'all':profile.free_all,
            'rate':profile.free_rate
        }, # 罚球
        'rebound':profile.rebound, # 篮板
        'steal':profile.steal, # 抢断
        'assist':profile.assist, # 助攻
        'turnover':profile.turnover, # 失误
        'block':profile.block, # 盖帽
        # 'players':[],
        'game':profile.game,
        'win':profile.win
    }
    return obj

def toPlayerProfileView(profile):
    obj={
        'point':profile.point,  #  得分
        'shot':{
            'in':profile.shot_in,
            'all':profile.shot_all,
            'rate':profile.shot_rate
        },  # 投篮
        'three':{
            'in':profile.three_in,
            'all':profile.three_all,
            'rate':profile.three_rate
        }, # 三分
        'free':{
            'in':profile.free_in,
            'all':profile.free_all,
            'rate':profile.free_rate
        }, # 罚球
        'rebound':profile.rebound, # 篮板
        'steal':profile.steal, # 抢断
        'assist':profile.assist, # 助攻
        'turnover':profile.turnover, # 失误
        'block':profile.block, # 盖帽
        # 'players':[],
        'game':profile.game,
        'doubledouble':profile.doubledouble,
        'threedouble':profile.threedouble
    }
    return obj


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)