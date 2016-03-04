# -*- coding: utf-8 -*-
import os
import datetime
import confiparse
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
    configParser = confiparse.ConfigParser()
    configParser.read(path);
    return configParser.get(option, key)

def setIniValue(path, option, key, value):
    configParser = confiparse.ConfigParser()
    configParser.read(path);
    configParser.set(option, key, value)
    configParser.write(open(path, 'w'))
    
def getTeamIdCode():
    return getIniValue(settings.ID_CODE_INI,'TEAM','id_code')

def setTeamIdCode(value):
    return setIniValue(ettings.ID_CODE_INI,'TEAM','id_code',value)

def getPlayerIdCode():
    return getIniValue(settings.ID_CODE_INI,'PLAYER','id_code')

def setPlayerIdCode(value):
    return setIniValue(ettings.ID_CODE_INI,'PLAYER','id_code',value)