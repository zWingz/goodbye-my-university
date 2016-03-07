# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics

@transaction.atomic
def register(postData):
    id_code = fileLogics.getUserIdCode()
    username = postData["username"]
    first_name = postData["first_name"]
    last_name = postData["last_name"]
    pwd = postData["password"]
    phone = postData["phone"]
    qq = postData["qq"]
    email = postData["email"]
    school = postData["school"]
    user = User.objects.create_user(username,email,pwd)
    user.id_code = id_code
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.qq = qq
    user.school = school
    user.status="normal"
    user.save()
    fileLogics.setUserIdCode(int(id_code)+1)
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