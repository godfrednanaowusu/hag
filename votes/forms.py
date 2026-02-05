from django import forms
from django.forms import ModelForm
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import *

