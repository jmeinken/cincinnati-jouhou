from __future__ import unicode_literals
import pretty

from django.db import models
from django.conf import settings
from django.utils.timezone import localtime

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
class event(TimeStampedModel):
    title       = models.CharField(max_length=255)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body        = models.TextField(max_length=1000)
    start_date  = models.DateField()
    start_time  = models.TimeField()
    end_time    = models.TimeField(blank=True, null=True)