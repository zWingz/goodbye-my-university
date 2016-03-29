from django.shortcuts import render
from django.http import HttpResponse
import json,datetime
from apps.message.models import News
from apps.game.models import Game
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
# Create your views here.
def welcome(request):
    news = News.objects.all().order_by("-create_time")[0:5]
    today = datetime.date.today()
    next_day = today+ datetime.timedelta(days=1)
    prev_day = today -  datetime.timedelta(days=1)
    today_game = Game.objects.filter(game_date=today.strftime("%Y-%m-%d"))
    next_day_game = Game.objects.filter(game_date=next_day.strftime("%Y-%m-%d"))
    prev_day_game = Game.objects.filter(game_date=prev_day.strftime("%Y-%m-%d"))
    return render(request,"index.html",{
            "todayGame":today_game,
            "nextDayGame":next_day_game,
            "prevDayGame":prev_day_game,
            "news":news
        })
