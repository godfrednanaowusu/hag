from django.contrib import admin
from .models import *
# Register your models here.

class AwardSchemesAdmin(admin.ModelAdmin):
	search_fields = ('year', 'name', 'theme', 'description', 'latest', 'active')
	list_display = ('year', 'name', 'theme', 'description', 'latest', 'active')  
admin.site.register(AwardSchemes, AwardSchemesAdmin)

class NominationCategoriesAdmin(admin.ModelAdmin):
	search_fields = ('scheme__name', 'year', 'name', 'description_short', 'image')
	list_display = ('scheme', 'year', 'name', 'description_short', 'image')  
admin.site.register(NominationCategories, NominationCategoriesAdmin)

class NominationsAdmin(admin.ModelAdmin):
	search_fields = ('referencenumber', 'nominee_code', 'category__year', 'category__name', 'shortlisted', 'approved', 'nominee_firstname', 'nominee_lastname', 'nominee_phonenumber', 'nominee_emailaddress', 'nominator_fullname', 'nominator_phonenumber', 'nominator_emailaddress')
	list_display = ('referencenumber', 'nominee_code', 'category', 'shortlisted', 'approved', 'nominee_firstname', 'nominee_lastname', 'nominee_phonenumber', 'nominee_emailaddress', 'nominator_fullname', 'nominator_phonenumber', 'nominator_emailaddress')  
admin.site.register(Nominations, NominationsAdmin)

