from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('nomination', NominationView.as_view(), name='nomination'),
	path('nomination_reference', NominationReferenceView.as_view(), name='nomination_reference'),
	path('nomination_form/', NominationFormView.as_view(), name='nomination_form'),
	path('nomination_form_thanks/', TemplateView.as_view(template_name='nomination_thanks.html'), name='nomination_form_thanks'),
	
	# path('create_refid', CreateRefidView.as_view(), name='create_refid'),
	# path('create_votecode', CreateVoteCodeView.as_view(), name='create_votecode'),

	# path('test_email', TestEmailView.as_view(), name='test_email'),
]