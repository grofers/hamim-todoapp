# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 06:52
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512)),
                ('scheduled_time', models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 30, 7, 52, 1, 444463, tzinfo=utc))),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('pending', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
