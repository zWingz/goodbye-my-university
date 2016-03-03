# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.IntegerField()),
                ('profile', models.CharField(max_length=20)),
                ('desc', models.TextField()),
                ('create_time', models.DateTimeField()),
                ('edit_tiime', models.DateTimeField()),
            ],
            options={
                'db_table': 'player',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=10)),
                ('logo', models.CharField(max_length=20)),
                ('profile', models.CharField(max_length=20)),
                ('desc', models.TextField()),
                ('campus', models.CharField(max_length=10)),
                ('create_time', models.DateTimeField()),
                ('edit_tiime', models.DateTimeField()),
                ('manager', models.ForeignKey(to_field='username', related_name='team', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'team',
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(related_name='players', to='team.Team'),
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile', to_field='username'),
        ),
    ]
