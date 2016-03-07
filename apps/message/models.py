import os
from django.db import models
import datetime
import json
from django import forms
from django.conf import settings
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics
# Create your models here.

class Message(models.Model):
    class Meta:
        db_table = 'message'
    id_code = models.CharField(max_length=10)
    sender = models.ForeignKey(User,to_field="username",related_name="send")
    receiver =models.ForeignKey(User,to_field="username",related_name="receive")
    content = models.CharField(max_length=200)
    msg_type = models.IntegerField()
    create_time = models.DateTimeField()
    status = models.IntegerField()  # 判断是否已读

    def save(self,*args,**kwargs):
        if not self.id_code:
            self.id_code = fileLogics.getIdCode("MESSAGE")
            self.create_time = datetime.datetime.now()
        super(Team, self).save(*args, **kwargs)
        fileLogics.setIdCode("MESSAGE",int(self.id_code)+1)

    def __str__(self):
        return self.id_code