from django.shortcuts import render
from django.shortcuts import redirect
# from django.shortcuts import render_to_response
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import apps.users.logics as Logics
from apps.message.models import Message
from apps.game.models import Game
from django.contrib.auth.models import User  
from django.db.models import Q
import datetime
from django.contrib.auth.views import logout as auth_logout
from utils.Decorator.decorator import post_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login,authenticate
# Create your views here.
def register(request):
    if request.method == 'POST':
        user = Logics.register(request.POST)
    if user:
        user = authenticate(username=request.POST['r-username'], password=request.POST['r-password'])
        auth_login(request,user)
        # return render(request, "auth/login.html")
    return redirect('/')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        pws = request.POST['password']
        user = authenticate(username=username, password=pws)
        if user :
            auth_login(request,user)
    # return render(request, "users/login.html")
    return redirect('/')
    # else:
        # return HttpResponseRedirect('/auth/login')

@login_required
def usercenter(request):
    status = request.user.status
    isManager = False;player = False;team = False;games = False;nextgames = False;
    player_data = {};team_data = {}
    if status == 'manager':
        team = request.user.team.all()[0]
        player = request.user.player
        player_data = Logics.getPlayerProfile(player.id_code)
        isManager = True
    elif status == 'player':
        player = request.user.player
        player_data = Logics.getPlayerProfile(player.id_code)
        team = player.team
    if team :
        team_data = Logics.getTeamProfile(team.id_code)
        now = datetime.datetime.now()
        weeknum = str(now.isocalendar()[0])+str(now.isocalendar()[1])
        games = Game.objects.filter(Q(team_one=team)|Q(team_two=team),weeknum=weeknum)
        nextgames =  Game.objects.filter(Q(team_one=team)|Q(team_two=team),weeknum=int(weeknum)+1)
    msg = Message.objects.filter(receiver=request.user).order_by("-create_time");
    return render(request,"users/usercenter.html",{
                                                                                                    "player":player,
                                                                                                    "player_data":player_data,
                                                                                                    "team":team,
                                                                                                    "team_data":team_data,
                                                                                                    "isManager":isManager,
                                                                                                    "games":games,
                                                                                                    "nextgames":nextgames,
                                                                                                    "msg":msg
                                                                                                    })


@login_required
def editUserInfo(request):
    response_data = {}
    if request.method == "POST":
        user = request.user
        result = Logics.editUserInfo(user,request.POST)
    if result:
        response_data['success'] = 1
        response_data['message'] = '修改成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '修改失败'
    return HttpResponse(json.dumps(response_data), content_type='application/json')

@login_required
def changePwd(request):
    response_data = {}
    response_data['success'] = 0
    response_data['message'] = '修改失败'
    if request.method == "POST":
        username = request.user.username
        oldPwd = request.POST['oldPwd']
        user = authenticate(username=username,password=oldPwd)
        if user is not None and user.is_active:
            newPwd = request.POST['newPwd']
            result = Logics.cheangePwd(user,newPwd)
            if result:
                response_data['success'] = 1
                response_data['message'] = '修改成功'
        else:
            response_data['message'] = '原密码错误'
    return HttpResponse(json.dumps(response_data),content_type='application/json')

@login_required
def  logout(request):
    auth_logout(request)
    return redirect('/')

# 用户头像更改view
@login_required
def updateImage(request):
    response_data = {}
    if request.method == 'POST':
        upfile = request.FILES['file']
        username = request.user.username
        extention =  upfile.name[upfile.name.rfind('.'):]
        fileName = str(int(time.time() * 10)) + extention
        with open(settings.USER_IMG + '/' + fileName, 'wb+') as dest:
            for chunk in upfile.chunks():
                dest.write(chunk)
        result = Logics.updateImage(username,fileName)
        if not result:
            response_data['success'] = 0
            response_data['message'] = '保存失败'
        else: 
            response_data['success'] = 1
            response_data['message'] = '保存成功'
            response_data['fileInfo']={
                                                    "filename":upfile.name,
                                                    "url":"/static/files/userImg/" + fileName,
                                                    "uname":fileName
                                                        };
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def editUser(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    user = User.objects.get(id_code=id_code)
    result = Logics.editUser(user,request.POST['username'],request.POST['first_name'],request.POST['last_name']
        ,request.POST['phone'],request.POST['email'],request.POST['qq'])
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
def deleteUser(request):
    id_code = request.POST.get("id_code","")
    response_data = {}
    if id_code != "":
        user = User.objects.get(id_code=id_code)
        user.delete()
        response_data['success'] = 1
        response_data['message'] = '操作成功'
    else:
        response_data['success'] = 0
        response_data['message'] = '操作失败'
    return HttpResponse(json.dumps(response_data),content_type="application/json")
