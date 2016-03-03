# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from django.contrib.auth.models import User  
from apps.users.models import Users
from django.contrib.auth import login as auth_login
@transaction.atomic
def register(postData):
    username = postData["username"]
    first_name = postData["first_name"]
    last_name = postData["last_name"]
    pwd = postData["password"]
    phone = postData["phone"]
    address = postData["address"]
    qq = postData["qq"]
    email = postData["email"]
    campus = postData["campus"]
    user = User.objects.create_user(username,email,pwd)
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.address = address
    user.qq = qq
    user.campus = campus
    user.save()
    return user

@transaction.atomic
def updateImage(username,imgpath):
    user = User.objects.get(username=username)
    user.img_path = imgpath
    user.save()
    return True

@transaction.atomic
def editUserInfo(username,postData):
    user = User.objects.get(username=username)
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

def aaa():
    pass;