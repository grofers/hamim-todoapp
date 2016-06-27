from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta

class User(models.Model):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    firstname = models.CharField(max_length=32, blank=False)
    lastname = models.CharField(max_length=32)
    email_verified = models.BooleanField(default=False, blank=True)

class Task(models.Model):
    user = models.ForeignKey('User', related_name='user_id')
    description = models.CharField(max_length=512, blank=False)
    scheduled_time = models.DateTimeField(
        default=(datetime.now()+timedelta(hours=1)), blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)
    pending = models.BooleanField(default=True, blank=True)
