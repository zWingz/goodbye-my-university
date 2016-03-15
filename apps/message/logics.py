# -*- coding: utf-8 -*-
import os
import json
import datetime
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.message.models import Message
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics


@transaction.atomic
def saveMsg(sender,receiver,title,content,msg_type):
    msg = Message()
    msg.sender = sender
    msg.receiver = receiver
    msg.title = title
    msg.content = content
    msg.msg_type = msg_type
    msg.status = 0
    msg.save()
    return True


@transaction.atomic
def readMsg(msg):
    msg.status = 1
    msg.save()
    return True


def getMsg(id_code):
    msg = Message.objects.get(id_code=id_code)
    return msg


def listMsg(user,status=0):
    msgs = Message.objects.filter(receiver=user,status=stataus)
    return msgs;


def listAllMsg(user):
    msgs = Message.objects.filter(receiver=user)
    return msgs;

