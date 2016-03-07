import os
from django.db import models
import datetime
import json
from django import forms
from django.conf import settings
from django.contrib.auth.models import User  
# Create your models here


class Team(models.Model):
    class Meta:
        db_table = 'team'
    id_code = models.CharField(max_length=10,null=True)
    name = models.CharField(max_length=10)
    manager = models.ForeignKey(User,to_field="username",related_name="team")
    logo = models.CharField(max_length=20,null=True)
    profile = models.CharField(max_length=20,null=True)
    desc = models.TextField()
    school = models.CharField(max_length=10,null=True)
    status = models.IntegerField(default=1)  # 判断是否生效字段
    create_time = models.DateTimeField()
    edit_tiime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
            self.status = 1
        self.edit_time = datetime.datetime.now()
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    class Meta:
        db_table = 'player'
    id_code = models.CharField(max_length=10,null=True)
    user = models.OneToOneField(User,to_field="username",related_name="player")  
    number = models.IntegerField(null=True)
    team = models.ForeignKey(Team,related_name="players",on_delete=models.CASCADE,null=True)
    profile = models.CharField(max_length=20)
    desc = models.TextField(null=True)
    position = models.CharField(max_length=5,null=True)
    status = models.IntegerField(default=1)  # 判断是否生效字段
    create_time = models.DateTimeField()
    edit_tiime = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
            status = 1
        self.edit_time = datetime.datetime.now()
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username 
 

