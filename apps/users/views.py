from django.shortcuts import render
from django.shortcuts import redirect
# from django.shortcuts import render_to_response
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import apps.users.logics as Logics
from apps.message.models import Message
from datetime import datetime
from django.contrib.auth.views import logout as auth_logout
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
    isManager = False;
    status = request.user.status
    player = False
    team = False
    player_data = {}
    team_data = {}
    if status == 'double':
        team = request.user.team.all()[0]
        player = request.user.player
        player_data = Logics.getPlayerProfile(player.id_code)
        # player_data = json.load(open(settings.PLAYER_PROFILE_DIR+"/"+player.profile,'r'));
        # team_data = json.load(open(settings.TEAM_PROFILE_DIR+"/"+team.profile+"/profile","r"))
        team_data = Logics.getTeamProfile(team.id_code)
        isManager = True
    elif status == 'player':
        player = request.user.player
        player_data = Logics.getPlayerProfile(player.id_code)
        team = player.team
    elif status == 'manager':
        team = request.user.team.all()[0]
        team_data = Logics.getTeamProfile(team.id_code)
        isManager = True
    msg = Message.objects.filter(receiver=request.user).order_by("-create_time");
    return render(request,"users/usercenter.html",{
                                                                                                    "player":player,
                                                                                                    "player_data":player_data,
                                                                                                    "team":team,
                                                                                                    "team_data":team_data,
                                                                                                    "isManager":isManager,
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
        with open(settings.UPLOADED_DIR + '/' + fileName, 'wb+') as dest:
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
                                                    "url":"/static/upload/" + fileName,
                                                    "uname":fileName
                                                        };
    return HttpResponse(json.dumps(response_data), content_type='application/json')
