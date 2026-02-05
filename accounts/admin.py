from django.contrib import admin

# Register your models here.
from .models import *

class RegisterAdmin(admin.ModelAdmin):
	search_fields = ('fullname', 'emailaddress', 'confirmed')
	list_display = ('fullname', 'emailaddress', 'confirmed')  
admin.site.register(Register, RegisterAdmin)


class AccountsAdmin(admin.ModelAdmin):
	search_fields = ('fullname', 'phonenumber', 'email', 'position', 'budget')
	list_display = ('fullname', 'phonenumber', 'email', 'position', 'budget')  
admin.site.register(Accounts, AccountsAdmin)


class UserActivityAdmin(admin.ModelAdmin):
	search_fields = ('user__fullname', 'activity', 'datecreated')
	list_display = ('user', 'activity', 'datecreated')  
admin.site.register(UserActivity, UserActivityAdmin)

class TelephonyAdmin(admin.ModelAdmin):
	search_fields = ('countrycode', 'country', 'supportednetworks', 'nonetstartwith')
	list_display = ('countrycode', 'country', 'supportednetworks', 'nonetstartwith')  
admin.site.register(Telephony, TelephonyAdmin)

class CountriesAdmin(admin.ModelAdmin):
	search_fields = ('name', 'nicename', 'iso', 'iso3', 'numcode', 'phonecode', 'minimum_nsn', 'maximum_nsn')
	list_display = ('name', 'nicename', 'iso', 'iso3', 'numcode', 'phonecode', 'minimum_nsn', 'maximum_nsn')  
admin.site.register(Countries, CountriesAdmin)
