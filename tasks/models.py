from __future__ import unicode_literals

from django.db import models
from datetime import datetime


class Task(models.Model):
    description = models.CharField(max_length=512, blank=False)
    scheduled_time = models.DateTimeField(default=datetime.now, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    pending = models.BooleanField(default=True)
    user_id = models.ForeignKey('users.User')
