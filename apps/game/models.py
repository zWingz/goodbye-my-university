import os
from django.db import models
import datetime
from django.conf import settings
from apps.team.models import Team
from django.contrib.auth.models import User 
import utils.files.logics as fileLogics
from mongoengine import *
# Create your models here.

class Game(models.Model):
    class Meta:
        db_table = 'game'
    id_code = models.CharField(max_length=10,null=True,unique=True)
    team_one = models.ForeignKey(Team,to_field='id_code',related_name="home_team")
    team_two = models.ForeignKey(Team,to_field='id_code',related_name="away_team")
    location = models.CharField(max_length=20)
    point = models.CharField(max_length=20)
    game_date = models.CharField(max_length=10,null=True)
    game_time = models.CharField(max_length=5,null=True)
    weeknum = models.CharField(max_length=10)
    week_index = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField()

    def save(self,*args,**kwargs):
        if not self.id_code:
            self.id_code = fileLogics.getIdCode("GAME")
            self.create_time = datetime.datetime.now()
        super(Game, self).save(*args, **kwargs)
        fileLogics.setIdCode("GAME",int(self.id_code)+1)

    def __str__(self):
        return self.id_code


connect('webbasketball',host=settings.MONGODB_CFG['host'],username=settings.MONGODB_CFG['username'])
class PlayerGameProfile(Document):
    id_code = StringField(max_length=10)
    name = StringField(max_length=10)
    point = IntField(required=False,default=0)
    shot_in = IntField(required=False,default=0)
    shot_all = IntField(required=False,default=0)
    shot_rate = FloatField(required=False,default=0)
    three_in = IntField(required=False,default=0)
    three_all = IntField(required=False,default=0)
    three_rate = FloatField(required=False,default=0)
    free_in = IntField(required=False,default=0)
    free_all = IntField(required=False,default=0)
    free_rate = FloatField(required=False,default=0)
    rebound = IntField(required=False,default=0)
    steal = IntField(required=False,default=0)
    assist = IntField(required=False,default=0)
    turnover = IntField(required=False,default=0)
    block = IntField(required=False,default=0)
    team_game = ReferenceField("TeamGameProfile")
    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = round(self.shot_in / self.shot_all*100,2)
        if self.three_all != 0:
            self.three_rate = round(self.three_in / self.three_all*100,2)
        if self.free_all != 0:
            self.free_rate = round(self.free_in / self.free_all*100,2)
        super(PlayerGameProfile, self).save(*args, **kwargs)

class TeamGameProfile(Document):
    id_code = StringField(max_length=10)
    name = StringField(max_length=10)
    point = IntField(required=False)
    shot_in = IntField(required=False)
    shot_all = IntField(required=False)
    shot_rate = FloatField(required=False)
    three_in = IntField(required=False)
    three_all = IntField(required=False)
    three_rate = FloatField(required=False)
    free_in = IntField(required=False)
    free_all = IntField(required=False)
    free_rate = FloatField(required=False)
    rebound = IntField(required=False)
    steal = IntField(required=False)
    assist = IntField(required=False)
    turnover = IntField(required=False)
    block = IntField(required=False)
    players = ListField(EmbeddedDocumentField("PlayerGameProfile"))
    def save(self, *args, **kwargs):
        if self.shot_all != 0:
            self.shot_rate = round(self.shot_in / self.shot_all*100,2)
        if self.three_all != 0:
            self.three_rate = round(self.three_in / self.three_all*100,2)
        if self.free_all != 0:
            self.free_rate = round(self.free_in / self.free_all*100,2)
        super(TeamGameProfile, self).save(*args, **kwargs)

class GameProfile(Document):
    id_code = StringField(max_length=10,unique=True)
    team_one_profile = ReferenceField(TeamGameProfile)
    team_two_profile = ReferenceField(TeamGameProfile)
