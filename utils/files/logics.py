# -*- coding: utf-8 -*-
import os
import datetime
import configparser
from django.conf import settings
import time
def saveFile(file,path):
    extention =  file.name[file.name.rfind('.'):]
    fileName = str(int(time.time() * 10)) + extention
    with open(path, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    return {fileName:file.name,fileUName:fileName}


def getIniValue(path, option, key):
    configParser = configparser.ConfigParser()
    configParser.read(path);
    return configParser.get(option, key)

def setIniValue(path, option, key, value):
    configParser = configparser.ConfigParser()
    configParser.read(path);
    configParser.set(option, key, value)
    configParser.write(open(path, 'w'))
  
def getUserIdCode():
    return getIniValue(settings.ID_CODE_INI,'USER','id_code')

def setUserIdCode(value):
    return setIniValue(settings.ID_CODE_INI,'USER','id_code',str(value))

def getTeamIdCode():
    return getIniValue(settings.ID_CODE_INI,'TEAM','id_code')

def setTeamIdCode(value):
    return setIniValue(settings.ID_CODE_INI,'TEAM','id_code',str(value))

def getPlayerIdCode():
    return getIniValue(settings.ID_CODE_INI,'PLAYER','id_code')

def setPlayerIdCode(value):
    return setIniValue(settings.ID_CODE_INI,'PLAYER','id_code',str(value))

def getMsgIdCode():
    return getIniValue(settings.ID_CODE_INI,'MESSAGE','id_code')

def setMsgIdCode(value):
    return setIniValue(settings.ID_CODE_INI,'MESSAGE','id_code',str(value))