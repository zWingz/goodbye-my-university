#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Hector Qiu <hectorqiuiscool@gmail.com>
#

"""

"""
from django.core.cache import get_cache
from django.contrib.auth.models import User
from utils.cfg import ThreadLocal

cache = get_cache("default")

USER_CACHE_TIMEOUT = 120  # 2min


def load_all_channel_admin_users():
    """加载全部用户"""

    cache_key = "channel_admin.apps.auth.models.users?type=list&host=%s"\
        % ThreadLocal.get_current_datasource_prefix()

    users = cache.get(cache_key)

    if not users:
        users = []

        qs = User.objects.using('game_channel_admin').all().order_by("id")
        if qs.exists():
            for user in qs:
                users.append(user)

        cache.set(cache_key, users, USER_CACHE_TIMEOUT)

    return users


def load_channel_admin_user(id, froce = False):
    """加载用户"""
    cache_key = "channel_admin.apps.auth.models.user?id=%s" % id

    user = cache.get(cache_key)
    if not user or froce:

        qs = User.objects.using('game_channel_admin').filter(id=id)

        if qs.exists():
            user = qs[0]

        cache.set(cache_key, user, USER_CACHE_TIMEOUT)

    return user


def load_admin_user(id, force_reload=False):
    """加载用户"""
    cache_key = "admin_user?id=%s" % id

    user = cache.get(cache_key)
    if not user or force_reload:

        qs = User.objects.filter(id=id)

        if qs.exists():
            user = qs[0]

        cache.set(cache_key, user, USER_CACHE_TIMEOUT)

    return user



def register_user():
    pass