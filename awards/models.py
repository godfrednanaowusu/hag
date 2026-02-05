from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .utils import generate_slug
from nominations.models import *

class Awards(models.Model):
	category = models.ForeignKey(NominationCategories, related_name="awards_category", blank=True, null=True, on_delete=models.SET_NULL, default='')
	nominee = models.ForeignKey(NominationCategories, related_name="awards_nominee", blank=True, null=True, on_delete=models.SET_NULL, default='')
	name = models.CharField(max_length=100, blank=True, null=True, default='')
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):  
		return str(self.name or '')
