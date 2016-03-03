# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20160303_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='campus',
        ),
    ]
