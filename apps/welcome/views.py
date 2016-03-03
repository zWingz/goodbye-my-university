from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
# Create your views here.
def welcome(request):
    return render(request,"index.html")
