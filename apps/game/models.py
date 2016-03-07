import os
from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import User 
# Create your models here.

class Game(models.Model):
    class Meta:
        db_table = 'game'
    id_code = models.CharField(max_length=10,null=True,unique=True)
    team_one = models.ForeignKey(Team,to_field='id_code')
    team_two = models.ForeignKey(Team,to_field='id_code')
    create_time = models.DateTimeField()
    data_profile = models.CharField(max_length=10)

    def save(self,*args,**kwargs):
        if not self.id_code:
            self.id_code = fileLogics.getIdCode("GAME")
            self.create_time = datetime.datetime.now()
        super(Team, self).save(*args, **kwargs)
        fileLogics.setIdCode("GAME",self.id_code+1)

    def __str__(self):
        return self.id_code