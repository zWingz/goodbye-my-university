# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.usual.views',
    url('^uploadFile$', 'uploadFile'),
    url('^dropFile$', 'dropFile'),
)