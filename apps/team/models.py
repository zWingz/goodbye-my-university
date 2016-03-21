import os
from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import User  
from mongoengine import *


# Create your models here


class Team(models.Model):
    class Meta:
        db_table = 'team'
    id_code = models.CharField(max_length=10,null=True,unique=True)
    name = models.CharField(max_length=10)
    manager = models.ForeignKey(User,to_field="username",related_name="team")
    logo = models.CharField(max_length=20,null=True)
    profile = models.CharField(max_length=20,null=True)
    desc = models.TextField()
    school = models.CharField(max_length=10,null=True)
    status = models.IntegerField(default=1)  # 判断是否生效字段
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()

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
    height = models.CharField(max_length=10,null=True)
    weight = models.CharField(max_length=10,null=True)
    profile = models.CharField(max_length=20)
    school = models.CharField(max_length=10,null=True)
    desc = models.TextField(null=True)
    position = models.CharField(max_length=5,null=True)
    status = models.IntegerField(default=1)  # 判断是否生效字段
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
            status = 1
        self.edit_time = datetime.datetime.now()
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username 
 
connect('webbasketball',host='192.168.201.67',username="zwing")
class TeamProfile(Document):
    id_code = StringField(max_length=10,unique=True)
    point = IntField(required=False)
    shot_in = IntField(required=False)
    shot_all = IntField(required=False)
    shot_rate = IntField(required=False)
    three_in = IntField(required=False)
    three_all = IntField(required=False)
    three_rate = IntField(required=False)
    free_in = IntField(required=False)
    free_all = IntField(required=False)
    free_rate = IntField(required=False)
    rebound = IntField(required=False)
    steal = IntField(required=False)
    assist = IntField(required=False)
    turnover = IntField(required=False)
    block = IntField(required=False)
    win = IntField(required=False)
    game = IntField(required=False)

    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = self.shot_in / self.shot_all
        if self.three_all != 0:
            self.three_rate = self.three_in / self.three_all
        if self.free_all != 0:
            self.free_rate = self.free_in / self.free_all
        super(TeamProfile, self).save(*args, **kwargs)

class PlayerProfile(Document):
    id_code = StringField(max_length=10,unique=True)
    point = IntField(required=False)
    shot_in = IntField(required=False)
    shot_all = IntField(required=False)
    shot_rate = IntField(required=False)
    three_in = IntField(required=False)
    three_all = IntField(required=False)
    three_rate = IntField(required=False)
    free_in = IntField(required=False)
    free_all = IntField(required=False)
    free_rate = IntField(required=False)
    rebound = IntField(required=False)
    steal = IntField(required=False)
    assist = IntField(required=False)
    turnover = IntField(required=False)
    block = IntField(required=False)
    doubledouble = IntField(required=False)
    threedouble = IntField(required=False)
    game = IntField(required=False)

    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = self.shot_in / self.shot_all
        if self.three_all != 0:
            self.three_rate = self.three_in / self.three_all
        if self.free_all != 0:
            self.free_rate = self.free_in / self.free_all
        super(PlayerProfile, self).save(*args, **kwargs)

