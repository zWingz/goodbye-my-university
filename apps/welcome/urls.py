#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'apps.welcome.views',
    url('', 'welcome'),
)
