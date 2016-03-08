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
  
def getIdCode(id_type):
    return getIniValue(settings.ID_CODE_INI,id_type,'id_code')


def setIdCode(id_type,value):
    return setIniValue(settings.ID_CODE_INI,id_type,'id_code',str(value))
