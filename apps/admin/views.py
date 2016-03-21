from django.shortcuts import render,redirect
import json, os, datetime
import copy
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# import apps.game.logics as Logics
from apps.game.models import Game
from apps.team.models import Team,TeamProfile
from utils.Decorator.decorator import post_required
from django.contrib.auth.decorators import login_required
import xlrd
# Create your views here.



def admin_index(request):
    return render(request,"layout/superuser-base.html");





# 比赛管理
def getFixtures(request):
    now = datetime.datetime.now()
    weeknum = request.GET.get('weeknum',str(now.isocalendar()[0])+str(now.isocalendar()[1])) 
    games = Game.objects.filter(weeknum=weeknum)

    next_weeknum = int(weeknum)+1
    next_games = Game.objects.filter(weeknum=next_weeknum)
    return render(request,"admin/game-list.html",{"title":"近期赛程","games":games,"nextgames":next_games})


def superuser_required(fnc):
    def wraper(request):
        if request.user.is_superuser:
            return fnc(request)
    return wraper