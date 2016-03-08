from django.shortcuts import render,redirect
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from apps.game.logics as Logics
from utils.Decorator.decorator import post_required
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