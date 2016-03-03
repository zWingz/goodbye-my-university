#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Youmi
#
"""
可以让db单独设置connection
@see http://stackoverflow.com/questions/3637419/multiple-database-config-in-django-1-2
"""

from utils.cfg import ThreadLocal

choose_list = ['game_data', 'game_log']

class DBRouter(object):
    """可以按照model里面的connection_name来设置要读的数据库"""

    def db_for_read(self, model, **hints):
        db_name = None
        if hasattr(model, 'connection_name'):
            if model.connection_name in choose_list:
                dbsource_str = ThreadLocal.get_current_dbsource()
                if dbsource_str:
                    db_name = '%s_%s' % (dbsource_str, model.connection_name)
        return db_name

    def db_for_write(self, model, **hints):
        db_name = None
        if hasattr(model, 'connection_name'):
            if model.connection_name in choose_list:
                dbsource_str = ThreadLocal.get_current_dbsource()
                if dbsource_str:
                    db_name = '%s_%s' % (dbsource_str, model.connection_name)
        return db_name

    def allow_syncdb(self, db, model):
        if hasattr(model, 'connection_name'):
            if model.connection_name in choose_list:
                dbsource_str = ThreadLocal.get_current_dbsource()
                if dbsource_str:
                    db_name = '%s_%s' % (dbsource_str, model.connection_name)
                    if db_name == db:
                        return True
        return None
