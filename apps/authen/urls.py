#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Account
    url(r'^login/$', 'apps.authen.views.login'),
    url(r'^register/$', 'apps.authen.views.register'),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {
        'post_change_redirect': '/authen/logout/'}),
    url(r'^logout/$', 'apps.authen.views.logout'),
)
