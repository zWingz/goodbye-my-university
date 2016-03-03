from django.db import models  
from django.contrib.auth.models import User  
from django.contrib.auth.admin import UserAdmin  
import datetime  

# 修改元类来扩展user
class ProfileBase(type):  
    def __new__(cls, name, bases, attrs):  #构造器，（名字，基类，类属性）
        module = attrs.pop('__module__')  
        parents = [b for b in bases if isinstance(b, ProfileBase)]  
        if parents:  
            fields = []  
            for obj_name, obj in attrs.items():  
                if isinstance(obj, models.Field): 
                    fields.append(obj_name)  
                User.add_to_class(obj_name, obj)       ####最重要的步骤
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)  
            UserAdmin.fieldsets.append((name, {'fields': fields}))  
        return type.__new__(cls, name, bases, attrs)  
class ProfileUser(object,metaclass=ProfileBase):  
    pass
class Users(ProfileUser):  
    phone= models.CharField(max_length = 20,null=True)
    qq = models.CharField(max_length=20,null=True)
    school = models.CharField(max_length=10,null=True)
    img_path = models.CharField(max_length=15,null=True)
    status = models.CharField(max_length=5,null=True) 
