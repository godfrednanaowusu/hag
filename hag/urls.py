from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('', include(('index.urls'))),
    path('', include(('nominations.urls'))),
    path('', include(('events.urls'))),
    path('', include(('awards.urls'))),
    path('', include(('accounts.urls'))),
    path('', include(('votes.urls'))),
    path('', include(('blog.urls'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
