#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Youmi
#
"""
可以让db单独设置connection
@see http://stackoverflow.com/questions/3637419/multiple-database-config-in-django-1-2
"""
from django.conf import settings


class DBRouter(object):
    """可以按照model里面的connection_name来设置要读的数据库"""
    def db_for_read(self, model, **hints):
        # 对于django内置的表，全部使用另外一个表
        db_name = None
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            db_name = settings.ADMIN_DATABASE
            if settings.READ_FROM_SLAVE:
                slave_db_name = "%s_slave" % db_name
                if slave_db_name in settings.DATABASES:
                    db_name = slave_db_name
        elif hasattr(model, 'connection_name'):
            db_name = model.connection_name
            # 如果有配置从库，使用从库进行读操作
            if settings.READ_FROM_SLAVE:
                slave_db_name = "%s_slave" % model.connection_name
                if slave_db_name in settings.DATABASES:
                    db_name = slave_db_name
        elif not hasattr(model, 'connection_name'):
            if 'default_slave' in settings.DATABASES:
                db_name = 'default_slave'
        return db_name

    def db_for_write(self, model, **hints):
        db_name = 'default'
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            db_name = settings.ADMIN_DATABASE
        elif hasattr(model, 'connection_name'):
            db_name = model.connection_name
        return db_name

    def allow_migrate(self, db, model):
        prefix = model.__module__.split('.')[0]
        if prefix == "django" or prefix == "utils":
            if db == settings.ADMIN_DATABASE:
                return True
            else:
                return False
        elif hasattr(model, 'connection_name'):
            if model.connection_name == db:
                return True
            else:
                return False
        else:
            if db == "default":
                return True
            else:
                return False
        return None
