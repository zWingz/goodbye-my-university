import os
from django.db import models
import datetime
from django.conf import settings
from apps.team.models import Team
from django.contrib.auth.models import User 
from mongoengine import *
# Create your models here.

class Game(models.Model):
    class Meta:
        db_table = 'game'
    id_code = models.CharField(max_length=10,null=True,unique=True)
    team_one = models.ForeignKey(Team,to_field='id_code',related_name="home_team")
    team_two = models.ForeignKey(Team,to_field='id_code',related_name="away_team")
    location = models.CharField(max_length=20)
    game_time = models.DateTimeField()
    weeknum = models.CharField(max_length=10)
    create_time = models.DateTimeField()
    data_profile = models.CharField(max_length=10)

    def save(self,*args,**kwargs):
        if not self.id_code:
            self.id_code = fileLogics.getIdCode("GAME")
            self.create_time = datetime.datetime.now()
        super(Game, self).save(*args, **kwargs)
        fileLogics.setIdCode("GAME",self.id_code+1)

    def __str__(self):
        return self.id_code


connect('webbasketball',host='192.168.201.67',username="zwing")
class PlayerGameProfile(Document):
    id_code = StringField(max_length=10)
    name = StringField(max_length=10)
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
    team_game = ReferenceField("TeamGameProfile")

class TeamGameProfile(Document):
    id_code = StringField(max_length=10)
    name = StringField(max_length=10)
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
    players = ListField(EmbeddedDocumentField("PlayerGameProfile"))


class GameProfile(Document):
    id_code = StringField(max_length=10)
    team_one_profile = ReferenceField(TeamGameProfile)
    team_two_profile = ReferenceField(TeamGameProfile)
