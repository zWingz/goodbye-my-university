# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_remove_team_campus'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='school',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
