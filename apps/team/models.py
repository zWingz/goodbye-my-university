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
    manager = models.ForeignKey(User,to_field="id_code",related_name="team")
    logo = models.CharField(max_length=20,default="teamImg.jpg")
    # profile = models.CharField(max_length=20,null=True)
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
    user = models.OneToOneField(User,to_field="id_code",related_name="player")  
    number = models.IntegerField(null=True)
    team = models.ForeignKey(Team,related_name="players",on_delete=models.CASCADE,null=True)
    height = models.CharField(max_length=10,null=True)
    weight = models.CharField(max_length=10,null=True)
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
 
connect('webbasketball',host=settings.MONGODB_CFG['host'],username=settings.MONGODB_CFG['username'])
class TeamProfile(Document):
    id_code = StringField(max_length=10,unique=True)
    point = IntField(required=False)
    avg_point = FloatField(required=False,default=0)
    shot_in = IntField(required=False)
    shot_all = IntField(required=False)
    shot_rate = FloatField(required=False,default=0)
    three_in = IntField(required=False)
    three_all = IntField(required=False)
    three_rate = FloatField(required=False,default=0)
    free_in = IntField(required=False)
    free_all = IntField(required=False)
    free_rate = FloatField(required=False,default=0)
    rebound = IntField(required=False)
    avg_rebound = FloatField(required=False,default=0)
    steal = IntField(required=False)
    avg_steal = FloatField(required=False,default=0)
    assist = IntField(required=False)
    avg_assist = FloatField(required=False,default=0)
    turnover = IntField(required=False)
    block = IntField(required=False)
    avg_block = FloatField(required=False,default=0)
    win = IntField(required=False)
    lose = IntField(required=False)
    win_rate = FloatField(required=False)
    game = IntField(required=False,default=0)

    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = round(self.shot_in / self.shot_all*100,2)
        if self.three_all != 0:
            self.three_rate = round(self.three_in / self.three_all*100,2)
        if self.free_all != 0:
            self.free_rate = round(self.free_in / self.free_all*100,2)
        if self.game != 0:
            self.win_rate = round(self.win / self.game*100,2)
            self.avg_point = round(self.point / self.game,1)
            self.avg_assist = round(self.assist / self.game,1)
            self.avg_block = round(self.block / self.game,1)
            self.avg_rebound = round(self.rebound / self.game,1)
            self.avg_steal = round(self.steal / self.game,1)
        self.lose = self.game - self.win
        super(TeamProfile, self).save(*args, **kwargs)

class PlayerProfile(Document):
    id_code = StringField(max_length=10,unique=True)
    point = IntField(required=False)
    avg_point = FloatField(required=False,default=0)
    shot_in = IntField(required=False)
    shot_all = IntField(required=False)
    shot_rate = FloatField(required=False,default=0)
    three_in = IntField(required=False)
    three_all = IntField(required=False)
    three_rate = FloatField(required=False,default=0)
    free_in = IntField(required=False)
    free_all = IntField(required=False)
    free_rate = FloatField(required=False,default=0)
    rebound = IntField(required=False)
    avg_rebound = FloatField(required=False,default=0)
    steal = IntField(required=False)
    avg_steal = FloatField(required=False,default=0)
    assist = IntField(required=False)
    avg_assist = FloatField(required=False,default=0)
    turnover = IntField(required=False)
    block = IntField(required=False)
    avg_block = FloatField(required=False,default=0)
    doubledouble = IntField(required=False)
    threedouble = IntField(required=False)
    game = IntField(required=False)

    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = round(self.shot_in / self.shot_all*100,2)
        if self.three_all != 0:
            self.three_rate = round(self.three_in / self.three_all*100,2)
        if self.free_all != 0:
            self.free_rate = round(self.free_in / self.free_all*100,2)
        if self.game != 0:
            self.avg_point = round(self.point / self.game,1)
            self.avg_assist = round(self.assist / self.game,1)
            self.avg_block = round(self.block / self.game,1)
            self.avg_rebound = round(self.rebound / self.game,1)
            self.avg_steal = round(self.steal / self.game,1)
        super(PlayerProfile, self).save(*args, **kwargs)

