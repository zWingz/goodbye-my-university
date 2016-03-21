# -*- coding: utf-8 -*-
import os
import json
import datetime
from django import forms
from django.conf import settings
from django.db import transaction
from django.db import models  
from apps.game.models import Game
from apps.team.models import Team
from django.contrib.auth.models import User  
import utils.files.logics as fileLogics
import copy 


