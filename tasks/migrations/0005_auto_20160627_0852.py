# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-27 08:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20160627_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='scheduled_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 6, 27, 9, 52, 9, 29762)),
        ),
    ]