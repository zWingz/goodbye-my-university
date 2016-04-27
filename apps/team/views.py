from django.shortcuts import render,redirect
import json, os, datetime
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import apps.team.logics as Logics
import apps.message.logics as MsgLogics
from apps.team.models import Team,Player
from apps.game.models import Game,TeamGameProfile,PlayerGameProfile
from apps.game.logics import saveGame
from apps.message.models import Message
from utils.files.logics import saveFile
from utils.Decorator.decorator import post_required
from django.contrib.auth.models import User  
from django.db.models import Q
# Create your views here.

# 球队列表
def listTeam(request):
    user = request.user
    count = int(settings.PAGE_COUNT)
    if request.method == "GET":  # 首次加载时候通过Get方法
        teamList = Team.objects.all().order_by("-create_time")[0:count];
        return render(request,"team/listTeam.html",{"teamList":teamList})
    else: # POST请求用于加载更多(分页)
        response_data = {}
        page = int(request.POST.get("page",1))
        teamList = Team.objects.all().order_by("-create_time")[(page-1)*count:page*count]
        if not user.is_authenticated():
            response_data['is_free_player'] = False #判断用户是否可以进行加入申请
        else:
            try:
                if user.player and not user.player.team:
                    response_data['is_free_player'] = True
                else:
                    response_data['is_free_player'] = False
            except:
                response_data['is_free_player'] = False
        response_data['teams'] = toTeamView(teamList)
        for each in response_data['teams']:
            if not user.is_authenticated() or not user.team.first() or each['id_code'] == user.team.first().id_code:
                each['can_inivite'] = False;  # 判断用户是否可以进行比赛邀请
            else:
                each['can_inivite'] = True;
        return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type="application/json")

@post_required
def listAllTeam(request):
    teamList = Team.objects.filter(status=1)
    return HttpResponse(json.dumps(toTeamView(teamList),cls=CJsonEncoder),content_type="application/json")


def listPlayer(request):
    count = int(settings.PAGE_COUNT)
    if request.method == "GET": 
        playerList = Player.objects.all().order_by("-create_time")[0:count];
        return render(request,"team/listPlayer.html",{"playerList":playerList})
    else:
        response_data = {}
        page = int(request.POST.get("page",1))
        playerList = Player.objects.all().order_by("-create_time")[(page-1)*count:page*count]
        if  request.user.is_authenticated() and request.user.team.first():
            response_data['is_manager'] = True
        else:  
            response_data['is_manager'] = False
        response_data['players'] = toPlayersView(playerList)
        # playerList = Player.objects.all()
        return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type="application/json")

# 球队详情
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
        if team in otherTeam:
            index = otherTeam.index(team)
            del otherTeam[index]
        return render(request,"team/teamDetail.html",{"team":team,"players":players,"team_data":data,"games":games,"nextgames":nextgames,"otherTeam":otherTeam})
    else:
        response_data ={}
        response_data['team'] = toTeamView([team])
        response_data['players'] = players
        response_data['team_data'] = toTeamProfileView(data)
        return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type='application/json')

def playerDetail(request):
    if request.method == 'GET':
        id_code = request.GET['id_code']
        player = Player.objects.get(id_code=id_code);
        data = Logics.getPlayerProfile(id_code)
        player_game_profile = PlayerGameProfile.objects.filter(id_code=player.id_code).order_by("-_id")[0:5]
        games = []
        for each in player_game_profile:
            game_id_code = each.team_game.game_id_code
            games.append(Game.objects.get(id_code=game_id_code))
        if player.team is not None:
            teammates = list(player.team.players.all())
            teammates.remove(player)
        else:
            teammates = []
        return render(request,"team/playerDetail.html",{"player":player,"player_data":data,"teammates":teammates,"games":games})
    else:
        id_code = request.POST['id_code']
        player = Player.objects.get(id_code=id_code);
        response_data ={}
        response_data['players'] = toPlayersView([player])
        return HttpResponse(json.dumps(response_data,cls=CJsonEncoder),content_type='application/json')


# Team do something view
@login_required
@post_required
def saveTeam(request):
    response_data = {}
    response_data['success'] = 0
    response_data['message'] = '保存失败'
    result = Logics.saveTeam(request.user,request.POST)
    if result :
        response_data['success'] = 1
        response_data['message'] = '保存成功'
    return redirect('/users/usercenter#user-team')

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
        fileInfo = saveFile(upfile,os.path.join(settings.TEAM_IMG))
        result = Logics.changeLogo(team,fileInfo['fileUName'])
        if result:
            response_data['success'] = 1
            response_data['message'] = '修改成功'
            response_data['fileInfo']={
                                                    "filename":fileInfo['fileName'],
                                                    "url":"/static/files/teamLogo/" + fileInfo['fileUName'],
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



# player do something
@post_required
@login_required
def savePlayer(request):
    url = request.get_full_path()
    print(url)
    response_data = {}
    response_data["success"] = 0
    response_data["message"] = '保存失败'
    result = Logics.savePlayer(request.user,request.POST)
    if result:
        response_data["success"] = 1
        response_data["message"] = '保存成功'
    return redirect('/users/usercenter#user-player')

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


# 同意邀请入队
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

# 同意邀请比赛
@login_required
@post_required
def agreeInviteGame(request):
    response_data = {}
    postData = request.POST
    team_one = Team.objects.get(manager=User.objects.get(id_code=request.POST['id_code']),status=1)
    msg = Message.objects.get(id_code=request.POST['msg_id_code'])
    team_two = Team.objects.get(manager=request.user,status=1)
    game_date = postData['game-date']
    if len(Game.objects.filter(Q(team_one = team_one)|Q(team_two = team_one),game_date=game_date)) != 0:
        response_data['success'] = 0
        response_data['message'] = team_one.name+"当天有比赛.该邀请无效"
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    if len(Game.objects.filter(Q(team_one = team_two)|Q(team_two = team_two),game_date=game_date)) != 0:
        response_data['success'] = 0
        response_data['message'] = "你的球队当天有比赛.该邀请无效"
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    result = saveGame(team_one,team_two,game_date,postData['game-time'],postData['location'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '生成比赛成功'
        MsgLogics.readMsg(msg)
    return HttpResponse(json.dumps(response_data),content_type="application/json")


@login_required
@post_required
def leaveTeam(request):
    response_data = {}
    id_code = request.POST['id_code']
    player = Player.objects.get(id_code=id_code)
    team = player.team
    if player is None :
        response_data['success'] = 0
        response_data['message'] = '离队失败'
    elif  team.manager == player.user:
        response_data['success'] = 0
        response_data['message'] = '该球员是管理者不能离队'
    else:
        result = Logics.leaveTeam(player)
        if result:
            response_data['success'] = 1
            response_data['message'] = '离队成功'
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
        if player.team is not None:
            obj['team'] = player.team.name
        else:
            obj['team'] = '无'
        result.append(obj)
    return result

def toTeamView(team):
    obj = []
    for each in team:
        tmp = {}
        tmp['id_code'] = each.id_code
        tmp['logo'] = each.logo
        tmp['name'] = each.name
        tmp['manager'] = each.manager.first_name
        tmp['school'] = each.school
        tmp['create_time'] = each.create_time
        tmp['desc'] = each.desc
        obj.append(tmp)
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



def  adeditPlayer(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    player = Player.objects.get(id_code=id_code)
    result = Logics.adeditPlayer(player,request.POST['number'],request.POST['height'],request.POST['weight'],request.POST['position'],request.POST['school'],request.POST['desc'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '操作成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
# @admin_required
def deletePlayer(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    response_data['success'] = 0
    response_data['message'] = '操作失败'
    if id_code != "" :
        player = Player.objects.get(id_code=id_code)
        if player.user.status == 'manager':
            response_data['success'] = 0
            response_data['message'] = '该球员是管理者,请先解散其球队'
        else:
            result = Logics.deletePlayer(player)
            if result:
                response_data['success'] = 1
                response_data['message'] = '操作成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")






def  adeditTeam(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    team = Team.objects.get(id_code=id_code)
    result = Logics.adeditTeam(team,request.POST['name'],request.POST['school'],request.POST['desc'])
    if result:
        response_data['success'] = 1
        response_data['message'] = '操作成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
# @admin_required
def deleteTeam(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    if id_code != "":
        result = Logics.deleteTeam(id_code)
        if result:
            response_data['success'] = 1
            response_data['message'] = '操作成功'
            return HttpResponse(json.dumps(response_data),content_type="application/json")
    response_data['success'] = 0
    response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")
