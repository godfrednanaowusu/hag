from django.contrib import admin
from .models import *
# Register your models here.

class PaymentRequestsAdmin(admin.ModelAdmin):
	search_fields = ('payment_processor', 'paymenttype', 'clientrefid', 'value', 'valuename', 'custom_code', 'paid', 'datepaid')
	list_display = ('payment_processor', 'paymenttype', 'clientrefid', 'amount', 'value', 'valuename', 'custom_code', 'paid', 'datepaid')  
admin.site.register(PaymentRequests, PaymentRequestsAdmin)

class PaymentsAdmin(admin.ModelAdmin):
	search_fields = ('request__clientrefid', 'nomination__nominee_firstname', 'nomination__nominee_lastname', 'transactionid', 'grossamount', 'transactionamount', 'netamount', 'datecreated')
	list_display = ('request', 'nomination', 'transactionid', 'grossamount', 'transactionamount', 'netamount', 'datecreated')  
admin.site.register(Payments, PaymentsAdmin)

class VotesAdmin(admin.ModelAdmin):
	search_fields = ('nomination__nominee_firstname', 'nomination__nominee_lastname', 'payment__transactionid', 'votecount')
	list_display = ('nomination', 'payment', 'votecount')  
admin.site.register(Votes, VotesAdmin)

class VoteSessionsAdmin(admin.ModelAdmin):
	search_fields = ('network', 'session_id', 'mode', 'msisdn', 'userdata', 'response_to_user', 'trafficid', 'nominee_code', 'datecreated')
	list_display = ('network', 'session_id', 'mode', 'msisdn', 'userdata', 'response_to_user', 'trafficid', 'nominee_code', 'datecreated')  
admin.site.register(VoteSessions, VoteSessionsAdmin)

class WigalCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('status', 'clienttransid', 'clientreference', 'reason')
	list_display = ('status', 'clienttransid', 'clientreference', 'reason')  
admin.site.register(WigalCallbacks, WigalCallbacksAdmin)

class USSDCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('status', 'clienttransid', 'clientreference', 'reason')
	list_display = ('status', 'clienttransid', 'clientreference', 'reason')  
admin.site.register(USSDCallbacks, USSDCallbacksAdmin)

class CardCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('status', 'transactionid', 'clienttransid', 'reason')
	list_display = ('status', 'transactionid', 'clienttransid', 'reason')  
admin.site.register(CardCallbacks, CardCallbacksAdmin)

class CashoutCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('status', 'clienttransid', 'clientreference', 'reason')
	list_display = ('status', 'clienttransid', 'clientreference', 'reason')  
admin.site.register(CashoutCallbacks, CashoutCallbacksAdmin)

class MyBusinessPayPaymentCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('status', 'amount', 'transaction_uuid', 'metadata_order_id', 'payment_date', 'datecreated')
	list_display = ('status', 'amount', 'transaction_uuid', 'metadata_order_id', 'payment_date', 'datecreated')  
admin.site.register(MyBusinessPayPaymentCallbacks, MyBusinessPayPaymentCallbacksAdmin)

class HubtelCallbacksAdmin(admin.ModelAdmin):
	search_fields = ('message', 'responseCode', 'data', 'datecreated')
	list_display = ('message', 'responseCode', 'data', 'datecreated')  
admin.site.register(HubtelCallbacks, HubtelCallbacksAdmin)

