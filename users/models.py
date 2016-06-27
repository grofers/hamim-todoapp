from __future__ import unicode_literals

import hashlib

from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=254, unique=True, blank=False)
    password = models.CharField(max_length=32, blank=False)
    firstname = models.CharField(max_length=32, blank=False)
    lastname = models.CharField(max_length=32)
    email_verified = models.BooleanField(default=False)
