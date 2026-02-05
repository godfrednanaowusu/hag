from django.contrib import admin
from .models import *
# Register your models here.

class AwardsAdmin(admin.ModelAdmin):
	search_fields = ('category__year', 'category__name', 'nominee__firstname', 'nominee__lastname', 'name')
	list_display = ('category', 'nominee', 'name')  
admin.site.register(Awards, AwardsAdmin)

