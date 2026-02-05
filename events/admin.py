from django.contrib import admin
from .models import *
# Register your models here.

class EventsAdmin(admin.ModelAdmin):
	search_fields = ('title', 'image', 'content')
	list_display = ('title', 'image', 'content')  
admin.site.register(Events, EventsAdmin)

