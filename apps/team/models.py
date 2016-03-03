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
    name = models.CharField(max_length=10)
    manager = models.ForeignKey(User,to_field="username",related_name="team")
    logo = models.CharField(max_length=20,null=True)
    profile = models.CharField(max_length=20,null=True)
    desc = models.TextField()
    school = models.CharField(max_length=10,null=True)
    create_time = models.DateTimeField()
    edit_tiime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        self.edit_time = datetime.datetime.now()
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    class Meta:
        db_table = 'player'
    user = models.OneToOneField(User,to_field="username",related_name="profile")  
    number = models.IntegerField()
    team = models.ForeignKey(Team,related_name="players",on_delete=models.CASCADE)
    profile = models.CharField(max_length=20)
    desc = models.TextField()
    create_time = models.DateTimeField()
    edit_tiime = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        self.edit_time = datetime.datetime.now()
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username 
 

