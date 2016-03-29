from django.shortcuts import render,redirect
import json, os, datetime
import copy
from django.conf import settings
from django.http import HttpResponse
# import apps.game.logics as Logics
from apps.game.models import Game
from apps.team.models import Team,TeamProfile
from apps.message.models import News
from utils.Decorator.decorator import post_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login,authenticate
from django.contrib.auth.models import User  
import xlrd
from utils.files.logics import saveFile
# Create your views here.



def admin_index(request):
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return render(request,"admin/login.html")
    else:
        return render(request,"layout/superuser-base.html")

def loginAdmin(request):
    print("login")
    if request.method == "POST":
        print("login post")
        username = request.POST['username']
        pws = request.POST['password']
        user = authenticate(username=username, password=pws)
        if user and user.is_superuser:
            auth_login(request,user)
    # return render(request, "users/login.html")
    return redirect('/admin/')




# 比赛管理
def getFixtures(request):
    now = datetime.datetime.now()
    weeknum = request.GET.get('weeknum',str(now.isocalendar()[0])+str(now.isocalendar()[1])) 
    games = Game.objects.filter(weeknum=weeknum)
    next_weeknum = int(weeknum)+1
    next_games = Game.objects.filter(weeknum=next_weeknum)
    return render(request,"admin/game-list.html",{"title":"近期赛程","games":games,"nextgames":next_games})


def createNews(request):
    return render(request,"admin/createnews.html")



@login_required
@post_required
def uploadImg(request):
    upfile = request.FILES['file']
    response_data = {}
    fileInfo = saveFile(upfile,os.path.join(settings.UPLOADED_DIR))
    if fileInfo:
        response_data['success'] = 1
        response_data['message'] = '修改成功'
        response_data['fileInfo']={
                                                "filename":fileInfo['fileName'],
                                                "url":"/static/upload/" + fileInfo['fileUName'],
                                                "uname":fileInfo['fileUName']
                                                    };
    return HttpResponse(json.dumps(response_data),content_type="application/json")



def superuser_required(fnc):
    def wraper(request):
        if request.user.is_superuser:
            return fnc(request)
    return wraper


def getUserList(request):
    return render(request,"admin/userList.html")