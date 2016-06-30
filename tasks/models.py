from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Task(models.Model):
    owner = models.ForeignKey('auth.User', related_name='user')
    description = models.CharField(max_length=512, blank=False)
    scheduled_time = models.DateTimeField(
        default=(timezone.now()+timedelta(hours=1)), blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)
    pending = models.BooleanField(default=True, blank=True)
