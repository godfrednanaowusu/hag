from django.contrib import admin
from .models import *
# Register your models here.


class TestimoniesAdmin(admin.ModelAdmin):
	search_fields = ('fullname', 'subinfo', 'testimony', 'photograph')
	list_display = ('fullname', 'subinfo', 'testimony', 'photograph')  
admin.site.register(Testimonies, TestimoniesAdmin)

class HAGTeamAdmin(admin.ModelAdmin):
	search_fields = ('fullname', 'position', 'bio', 'photograph', 'teammember', 'boardmember', 'active')
	list_display = ('fullname', 'position', 'bio', 'photograph', 'teammember', 'boardmember', 'active')  
admin.site.register(HAGTeam, HAGTeamAdmin)

class GalleriesAdmin(admin.ModelAdmin):
	search_fields = ('title', 'image')
	list_display = ('title', 'image')  
admin.site.register(Galleries, GalleriesAdmin)

class EmailSubscriptionAdmin(admin.ModelAdmin):
	search_fields = ('email', 'subscriptionstatus', 'code', 'datecreated')
	list_display = ('email', 'subscriptionstatus', 'code', 'datecreated')  
admin.site.register(EmailSubscription, EmailSubscriptionAdmin)

