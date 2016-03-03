# -*- coding: utf-8 -*-

import json, os, time
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
import apps.usual.logics as Logics


@login_required
def uploadFile(request):
    response_data = {}
    if request.method == 'POST':
        upfile = request.FILES['file']
        extention =  upfile.name[upfile.name.rfind('.'):]
        fileName = str(int(time.time() * 10)) + extention
        with open(settings.UPLOADED_DIR + '/' + fileName, 'wb+') as dest:
            for chunk in upfile.chunks():
                dest.write(chunk)
        response_data['success'] = 1
        response_data['message'] = '保存成功'
        response_data['fileInfo']={
                                                "filename":upfile.name,
                                                "url":"/static/upload/" + fileName,
                                                "uname":fileName
                                                    };

    return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
def dropFile(request):
    response_data = {}
    if request.method == 'POST':
        fileName = request.POST['fileName']
        fileFullname = settings.UPLOADED_DIR + '/' + fileName
        os.remove(fileFullname)
    response_data['success'] = 1
    response_data['message'] = '删除成功'
    response_data['data'] = fileName
    return HttpResponse(json.dumps(response_data), content_type='application/json')