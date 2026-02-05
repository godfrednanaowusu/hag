from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('votes_ussd', VotesUSSDView.as_view(), name='votes_ussd'),
	path('votes_online', VotesOnlineView.as_view(), name='votes_online'),
	
	path('wigal-callback/', WigalCallbackView.as_view(), name='wigal_callback'),
	path('payment-successful/', WigalCardSuccessfulCallbackView.as_view(), name='wigal_card_successful_callback'),
	path('payment-failed/', WigalCardFailureCallbackView.as_view(), name='wigal_card_failure_callback'),
	path('wigal-cashout-callback/', WigalCashoutCallbackView.as_view(), name='wigal_cashout_callback'),
	
	path('mybusinesspay-payment-callback/', MyBusinessPayPaymentCallbackView.as_view(), name='mybusinesspay_payment_callback'),
	path('mybusinesspay-payment-thankyou/', MyBusinessPayPaymentThankYouView.as_view(), name='mybusinesspay_payment_thankyou'),
	path('mybusinesspay-payment-posturl/', MyBusinessPayPaymentPostURLView.as_view(), name='mybusinesspay_payment_posturl'),
	
	path('asoribaland_payment_successful/', AsoribaLandPaymentSuccessfulView.as_view(), name='asoribaland_payment_successful'),

	path('hubtel-ussd-callback/', HubtelCallbackView.as_view(), name='hubtel_ussd_callback'),
	path('hubtel-return-callback/', HubtelReturnCallbackView.as_view(), name='hubtel_return_callback'),
	path('hubtel-cancel-callback/', HubtelCancelCallbackView.as_view(), name='hubtel_cancel_callback'),
	
]