from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .views import BlogView, BlogDetailView

urlpatterns = [
	path('blog/', BlogView.as_view(), name='blog'),   
    path('blog/<str:identifier>', BlogDetailView.as_view(), name='blog_detail'), 
	
]