from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .utils import generate_slug
from hag.storage_backends import *
from uuid import uuid4
import uuid

import os

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

class Testimonies(models.Model):
	fullname = models.CharField(max_length=255, blank=True, null=True )
	subinfo = models.CharField(max_length=255, blank=True, null=True )
	testimony = models.TextField(blank=True, null=True )
	photograph = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True)
	active = models.BooleanField(blank=True,  default=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return self.fullname

class HAGTeam(models.Model):
	fullname = models.CharField(max_length=255, blank=True, null=True )
	position = models.CharField(max_length=255, blank=True, null=True )
	bio = models.TextField(blank=True, null=True )
	photograph = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True)
	facebook = models.URLField(max_length=255, blank=True, null=True )
	twitter = models.URLField(max_length=255, blank=True, null=True )
	instagram = models.URLField(max_length=255, blank=True, null=True )
	linkedin = models.URLField(max_length=255, blank=True, null=True )
	teammember = models.BooleanField(blank=True,  default=False)
	boardmember = models.BooleanField(blank=True,  default=False)
	order_id = models.IntegerField(blank=True, null=True, default=1 )
	active = models.BooleanField(blank=True,  default=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return self.fullname

class Galleries(models.Model):
	image = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True)
	title = models.CharField(max_length=255, blank=True, null=True )
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return str(self.id)

class EmailSubscription(models.Model):
    code = models.UUIDField(default=uuid.uuid4)
    email = models.EmailField(max_length=255, blank=False, null=True)
    subscriptionstatus = models.BooleanField(max_length=255, blank=True, default=False )
    # code = models.CharField(max_length=255, blank=False, null=True)
    datecreated = models.DateTimeField(default=timezone.now)


    def __str__(self):  
        return self.email

