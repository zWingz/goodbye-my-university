# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='campus',
            field=models.CharField(null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.CharField(null=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='team',
            name='profile',
            field=models.CharField(null=True, max_length=20),
        ),
    ]
