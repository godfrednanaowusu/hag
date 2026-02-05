from django.contrib import admin
from .models import *
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
	search_fields = ('title', 'artcover', 'content')
	list_display = ('title', 'artcover', 'content')  
admin.site.register(Blog, BlogAdmin)

