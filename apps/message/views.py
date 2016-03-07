from django.shortcuts import render
import json, os, time
from django.conf import settings
from django.http import HttpResponse
from apps.message.logo as Logics
from utils.Decorator.decorator import post_required
# Create your views here.

MSG_TYPE = {
    'join_team':1,
    "leave_team":2,
    "other":3
}

@login_required
@post_required
def sendMsg(request):
    response_data = {}
    response_data.success = 0
    response_data.message = '发送失败'
    sender = request.user
    receiver = User.objects.get(username=request.POST['receiver'])
    content = request.POST['content']
    msg_type = request.POST['type']
    result = Logics.saveMsg(sender,receiver,content,msg_type)
    if result:
        response_data.success = 1
        response_data.message = '发送成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
@post_required
def readMsg(request):
    msgs =  json.loads(request.POST['msgs'])
    for each in msgs:
        msg = Message.objects.get(id_code = each)
        Logics.readMsg(msg)
    response_data = {}
    response_data.success = 1
    response_data.message = '发送失败'
    return return HttpResponse(json.dumps(response_data),content_type="application/json")




@login_required
@post_required
def sendJoinTeamMsg(request):
    response_data = {}
    sender = request.user
    receiver = User.objects.get(username=request.POST['receiver'])
    content = receiver.first_name+"请求加入球队"
    msg_type = MSG_TYPE['join_team']
    result = Logics.saveMsg(sender,receiver,content,msg_type)
    if result:
        response_data.success = 1
        response_data.message = '申请成功'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

@login_required
def listUnReadMsg(request):
    msgs = logics.listMsg(request.user)
    return render(request,"message/listMsg.html",{msgs:msgs})

@login_required
def listAllMsg(request):
    msgs = logics.listAllMsg(request.user)
    return render(request,"message/listMsg.html",{msgs:msgs})

# @login_required

def unReadMsgCount(request):
    if request.user.is_authenticated(): 
        count = Message.objects.filter(receiver = request.user,status=0).count()
        return {
                            msgCount:count
                        }
    else:
        return {}