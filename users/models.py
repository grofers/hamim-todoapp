from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=128, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    firstname = models.CharField(max_length=128, blank=False)
    lastname = models.CharField(max_length=128)
    email_verified = models.BooleanField(default=False)
