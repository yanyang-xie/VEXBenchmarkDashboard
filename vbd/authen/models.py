# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32)
    permission = models.IntegerField(default=1)
    
    def delete(self, using=None):
        self.user.delete()

    def __unicode__(self):
        if hasattr(self, 'nickname') and self.nickname is not None:
            return self.nickname
        else:
            return self.user.username