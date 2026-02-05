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

class Events(models.Model):
	title = models.CharField(max_length=255, blank=True, null=True, default='')
	slug = models.SlugField(unique=True, null=True, blank=True, max_length=255, default='')
	image = models.ImageField(upload_to=path_and_rename, blank=True, null=True, default='')
	content = models.TextField(blank=True, null=True, default='')	
	featured = models.BooleanField(blank=True, default=False)	
	datecreated = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		try:
			if not self.is_update_view:
				self.slug = generate_slug(self, self.title)
		except:
			self.slug = generate_slug(self, self.title)

		super(Events, self).save(*args, **kwargs)
		

	def __str__(self):  
		return self.slug
