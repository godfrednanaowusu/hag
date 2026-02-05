from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('award/', AwardView.as_view(), name='award'),
	
]