from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .utils import generate_slug
from .validators import *
from hag.storage_backends import *

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
class AwardSchemes(models.Model):
	year = models.CharField(max_length=50, blank=True, null=True, default='')
	name = models.CharField(max_length=255, blank=True, null=True, default='')
	theme = models.CharField(max_length=255, blank=True, null=True, default='')
	description = models.TextField(blank=True, null=True, default='')
	image = models.ImageField(upload_to=path_and_rename, blank=True, null=True, validators=[validate_file_size])
	latest = models.BooleanField(blank=True, default=True)
	nominationopen = models.BooleanField(blank=True, default=True)
	votingopen = models.BooleanField(blank=True, default=True)
	active = models.BooleanField(blank=True, default=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return str(self.year or '') + ' ' + str(self.name or '')

class NominationCategories(models.Model):
	scheme = models.ForeignKey(AwardSchemes, related_name="nominations_awardscheme", blank=True, null=True, on_delete=models.SET_NULL, default='')
	year = models.CharField(max_length=50, blank=True, null=True, default='')
	name = models.CharField(max_length=255, blank=True, null=True, default='')
	description_short = models.TextField(blank=True, null=True, default='')
	description_long = models.TextField(blank=True, null=True, default='')
	image = models.ImageField(upload_to=path_and_rename, blank=True, null=True, validators=[validate_file_size])
	active = models.BooleanField(blank=True, default=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return str(self.scheme or '') + ' : ' + str(self.name or '')

class Nominations(models.Model):
	GENDER_CHOICES = (('Male','Male'), ('Female','Female'), ('NGO','NGO'))	
	AGEGROUP_CHOICES = (('10-20','10-20'), ('20-30','20-30'), ('30-40','30-40'), ('40-50','40-50'), ('50-60','50-60'), ('60-70','60-70'), ('70-80','70-80'), ('80-90','80-90'), ('90-100','90-100'))	
	category = models.ForeignKey(NominationCategories, related_name="nominations_category", blank=True, null=True, on_delete=models.SET_NULL, default='')
	referencenumber = models.CharField(max_length=200, blank=True, null=True, default='')
	nominee_photograph = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True, default='', validators=[validate_image_size])
	nominee_firstname = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_middlename = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_lastname = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_phonenumber = models.CharField(max_length=100, blank=True, null=True, default='')	
	nominee_emailaddress = models.EmailField(max_length=100, blank=True, null=True, default='')
	nominee_gender = models.CharField(max_length=100, blank=True, null=True, choices = GENDER_CHOICES, default='Female')
	nominee_agegroup = models.CharField(max_length=100, blank=True, null=True, choices = AGEGROUP_CHOICES, default='30-40')
	nominee_bio = models.TextField(blank=True, null=True, default='')
	nominee_deserve_info = models.TextField(blank=True, null=True, default='')
	nominee_effort_info = models.TextField(blank=True, null=True, default='')
	nominee_turning_point = models.TextField(blank=True, null=True, default='')
	nominee_exception = models.TextField(blank=True, null=True, default='')
	nominee_reference_links = models.TextField(blank=True, null=True, default='')
	nominee_towncity = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_region = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_country = models.CharField(max_length=100, blank=True, null=True, default='')
	nominee_code = models.CharField(max_length=100, blank=True, null=True, default='')
	company_logo = models.ImageField(upload_to=path_and_rename, max_length=255, blank=True, null=True, default='', validators=[validate_image_size])
	company_name = models.CharField(max_length=100, blank=True, null=True, default='')
	company_industry = models.CharField(max_length=100, blank=True, null=True, default='')
	company_bio = models.TextField(blank=True, null=True, default='')
	nominator_fullname = models.CharField(max_length=100, blank=True, null=True, default='')
	nominator_phonenumber = models.CharField(max_length=100, blank=True, null=True, default='')	
	nominator_emailaddress = models.EmailField(max_length=100, blank=True, null=True, default='')
	nominator_bio = models.TextField(blank=True, null=True, default='')
	nominator_knownnominee_time = models.CharField(max_length=100, blank=True, null=True, default='')
	nominator_nominee_relationship = models.CharField(max_length=100, blank=True, null=True, default='')
	shortlisted = models.BooleanField(blank=True, default=False)
	approved = models.BooleanField(blank=True, default=False)
	votable = models.BooleanField(blank=True, default=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return str(self.category or '') + ': ' + str(self.nominee_firstname or '') + ' ' + str(self.nominee_lastname or '')
