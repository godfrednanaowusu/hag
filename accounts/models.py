from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .utils import *
import os
from uuid import uuid4

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

# Create your models here.
class Register(models.Model):
    fullname = models.CharField(max_length=255, blank=True, null=True, default='')
    emailaddress = models.EmailField(max_length=255, blank=True, null=True, default='')
    code = models.CharField(max_length=100, blank=True, null=True, default='')
    confirmed = models.BooleanField(blank=False,  default=False)
    expired_date = models.BigIntegerField(blank=True, null=True, default=0)
    datecreated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):  
        return str(self.fullname)

class Accounts(models.Model):
    GENDER_CHOICES = (('Male','Male'), ('Female','Female'))
    user = models.ForeignKey(User, related_name="account_user", null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=100)
    photograph = models.ImageField(upload_to=path_and_rename, blank=True, null=True )
    fullname = models.CharField(max_length=100, blank=True, null=True )
    gender = models.CharField(max_length=50, null=True, blank=True, choices = GENDER_CHOICES, default = None) 
    phonenumber = models.CharField(max_length=100, blank=True, null=True )
    email = models.EmailField(blank=True, null=True )
    position = models.CharField(max_length=100, blank=True, null=True )
    budget = models.CharField(max_length=100, blank=True, null=True )
    code = models.CharField(max_length=100, blank=True, null=True )
    confirmed = models.BooleanField(blank=True, default=False)
    pastfirsttime = models.BooleanField(blank=True, default=False)
    admin = models.BooleanField(blank=True, default=False)
    active = models.BooleanField(blank=True, default=False)
    datecreated = models.DateTimeField(default=timezone.now)
    
    def save(self, *args, **kwargs):
        try:
            if not self.is_update_view:
                self.slug = generate_slug(self, self.fullname)
        except:
            self.slug = generate_slug(self, self.fullname)
        
        super(Accounts, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.slug)


class UserActivity(models.Model):
	"""This is them main log module used to store logs of a user's activity"""		
	user = models.ForeignKey(Accounts, related_name='activity_user', blank=True, null=True, on_delete=models.SET_NULL)
	activity = models.TextField(null=True, blank=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		# return self.user__memberid
		return self.activity

class Telephony(models.Model):	
    """This is where country codes and related things are stored, also this is used to format phonenumbers"""
    countrycode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    nowithcountrycode = models.IntegerField(null=True, blank=True)
    nowithoutcountrycode = models.IntegerField(null=True, blank=True)
    supportednetworks = models.CharField(max_length=200, null=True, blank=True)
    nonetstartwith = models.IntegerField(null=True, blank=True)
    datecreated = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        # return self.user__memberid
        return str(self.countrycode)


class Countries(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, default='') 
    nicename = models.CharField(max_length=100, null=True, blank=True, default='') 
    iso = models.CharField(max_length=100, null=True, blank=True, default='') 
    iso3 = models.CharField(max_length=100, null=True, blank=True, default='') 
    numcode = models.CharField(max_length=100, null=True, blank=True, default='') 
    phonecode = models.CharField(max_length=100, null=True, blank=True, default='') 
    minimum_nsn = models.IntegerField(null=True, blank=True, default=7) 
    maximum_nsn = models.IntegerField(null=True, blank=True, default=9)
	
    def __str__(self):  
        return str(self.name)
