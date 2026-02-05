from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .utils import generate_slug
# from hag.storage_backends import *
import os
from uuid import uuid4
import uuid
from hag.validators import *


# Create your models here.
def path_and_rename(instance, filename):
    upload_to = 'media'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Blog(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name='Title')
    artcover = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True, verbose_name='Art Cover')
    author = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Author' )
    location = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Location' )
    link = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name='Link' )
    content = models.TextField(blank=True, null=True )    
    active = models.BooleanField(blank=True, default=True)
    date = models.DateField(blank=False, null=True, verbose_name='Date Posted')
    datecreated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.title or '')
