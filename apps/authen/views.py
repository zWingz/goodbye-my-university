#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Youmi_OA
#
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import is_safe_url
from django.conf import settings
from django.contrib.auth.views import logout as auth_logout
from django.contrib.auth.decorators import login_required
# from utils.http.httputil import get_client_ip
from datetime import datetime
import json
import sys
import logging

# login_logger = logging.getLogger("login")

def login(request):
    form = AuthenticationForm()
    redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')
    if request.method == "POST":
        resp = None
        # ip = get_client_ip(request)
        log_post = request.POST.copy()
        log_post['password'] = '*****'
        log_result = 'FAIL-RECAPTCHA_EMPTY'
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            log_result = "SUCCESS"
            resp = HttpResponseRedirect(redirect_to)
        else:
            print(form.errors)
        #     log_result = 'FAIL-PASSWORD-ERROR'

        # login_msg = "%s - [LOGIN][%s]- ip: %s, POST: %s, GET: %s, UA: %s, REFER: %s, HTTP_X_FORWARDED_FOR: %s" % (
        #     datetime.now().strftime("%Y-%m-%d %H:%M:%S %p"),
        #     log_result,
        #     ip,
        #     json.dumps(log_post),
        #     json.dumps(request.GET),
        #     request.META.get('HTTP_USER_AGENT'),
        #     request.META.get('HTTP_REFERER'),
        #     request.META.get('HTTP_X_FORWARDED_FOR'),
        # )
        # login_logger.info(login_msg)
        # print(login_msg)
        if resp:
            return resp
    return render_to_response(
        'auth/login.html', {
            'error': request.GET.get("error", ""),
            'next': request.GET.get(REDIRECT_FIELD_NAME, ''),
            'form': form
        },
        context_instance=RequestContext(request)
    )


@login_required
def logout(request):
    """ 由于django自带的退出登录会跳到admin页面，这里处理一下跳转。  """
    auth_logout(request)
    return HttpResponseRedirect('/authen/login/')

def register(request):
    return HttpResponse("注册页面")