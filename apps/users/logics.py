# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from django.contrib.auth.models import User  
from apps.team.models import TeamProfile,PlayerProfile
import utils.files.logics as fileLogics

@transaction.atomic
def register(postData):
    id_code = fileLogics.getIdCode("USER")
    username = postData["r-username"]
    pwd = postData["r-password"]
    email = postData["r-email"]
    user = User.objects.create_user(username,email,pwd)
    user.id_code = id_code
    user.status="normal"
    user.save()
    fileLogics.setIdCode("USER",int(id_code)+1)
    return user

@transaction.atomic
def updateImage(username,imgpath):
    user = User.objects.get(username=username)
    user.img_path = imgpath
    user.save()
    return True

@transaction.atomic
def editUserInfo(user,postData):
    setPostToModel(user,postData)
    user.save()
    return True

@transaction.atomic
def cheangePwd(user,pwd):
    user.set_password(pwd)
    user.save()
    return True



def setPostToModel(model, post):
    for key, value in post.items():
        setattr(model, key, value)


def getTeamProfile(id_code):
    profile = TeamProfile.objects.get(id_code=id_code)
    return profile

def getPlayerProfile(id_code):
    profile = PlayerProfile.objects.get(id_code=id_code)
    return profile