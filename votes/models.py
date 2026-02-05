from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from hag.storage_backends import *
from nominations.models import *
from uuid import uuid4

class PaymentRequests(models.Model):
    PAYMENTPROCESSOR_CHOICES = (('redde','redde'), ('mybusinesspay','mybusinesspay'), ('paypal','paypal'), ('hubtel','hubtel'))	
    PAYMENTTYPE_CHOICES = (('ussd','ussd'), ('card','card'), ('paypal','paypal'))	
    payment_processor = models.CharField(max_length=100, blank=True, null=True, choices=PAYMENTPROCESSOR_CHOICES, default='redde' )
    paymenttype = models.CharField(max_length=100, blank=True, null=True, choices=PAYMENTTYPE_CHOICES, default='ussd')
    clientrefid = models.UUIDField(default=uuid4)
    clienttransid = models.CharField(max_length=200, blank=True, null=True, default='')
    amount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    title = models.CharField(max_length=100, blank=True, null=True, default='')
    description = models.CharField(max_length=200, blank=True, null=True, default='')
    valuename = models.CharField(max_length=100, blank=True, null=True, default='')
    value = models.CharField(max_length=100, blank=True, null=True, default='')
    custom_code = models.CharField(max_length=100, blank=True, null=True, default='')
    
    payer_fullname = models.CharField(max_length=100, blank=True, null=True, default='')
    payer_phonenumber = models.CharField(max_length=100, blank=True, null=True, default='')
    payer_email = models.CharField(max_length=100, blank=True, null=True, default='')
    
    status = models.CharField(max_length=100, blank=True, null=True, default='')

    paid = models.BooleanField(blank=False, default=False)
    datepaid = models.DateField(null=True, blank=True, default='2020-01-01')     
    datecreated = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        return str(self.clientrefid or '')

class Payments(models.Model):
    request = models.ForeignKey(PaymentRequests, related_name="payments_request", blank=True, null=True, on_delete=models.SET_NULL, default='')
    nomination = models.ForeignKey(Nominations, related_name="payments_nomination", blank=True, null=True, on_delete=models.SET_NULL, default='')
    transactionid = models.CharField(max_length=255, blank=True, null=True, default='')    
    grossamount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    transactionamount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    netamount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    datecreated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):  
        return str(self.transactionid)

class Votes(models.Model):
    nomination = models.ForeignKey(Nominations, related_name="votes_nomination", blank=True, null=True, on_delete=models.SET_NULL, default='')
    payment = models.ForeignKey(Payments, related_name="votes_payment", blank=True, null=True, on_delete=models.SET_NULL, default='')
    votecount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    datecreated = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        return str(self.nomination or '') + ' ' + str(self.votecount or '')

class VoteSessions(models.Model):
    network = models.CharField(max_length=200, blank=True, null=True, default='')
    session_id = models.CharField(max_length=200, blank=True, null=True, default='')
    mode = models.CharField(max_length=200, blank=True, null=True, default='')
    msisdn = models.CharField(max_length=200, blank=True, null=True, default='')
    userdata = models.CharField(max_length=255, blank=True, null=True, default='')
    response_to_user = models.CharField(max_length=255, blank=True, null=True, default='')
    trafficid = models.CharField(max_length=255, blank=True, null=True, default='')
    other = models.CharField(max_length=255, blank=True, null=True, default='')
    nominee_code = models.CharField(max_length=100, blank=True, null=True, default='')
    session_step = models.CharField(max_length=100, blank=True, null=True, default='')
    datecreated = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        return str(self.network or '') + ' ' + str(self.session_id or '')

class WigalCallbacks(models.Model):
    status = models.CharField(max_length=200, blank=True, null=True, default='')
    clienttransid = models.CharField(max_length=200, blank=True, null=True, default='')
    clientreference = models.CharField(max_length=200, blank=True, null=True, default='')
    telcotransid = models.CharField(max_length=200, blank=True, null=True, default='')
    transactionid = models.CharField(max_length=200, blank=True, null=True, default='')
    brandtransid = models.CharField(max_length=200, blank=True, null=True, default='')
    reason = models.TextField(blank=True, null=True, default='')
    statusdate = models.CharField(max_length=200, blank=True, null=True, default='')
    
    def __str__(self):  
        return str(self.status or '')

class USSDCallbacks(models.Model):
    status = models.CharField(max_length=200, blank=True, null=True, default='')
    clienttransid = models.CharField(max_length=200, blank=True, null=True, default='')
    clientreference = models.CharField(max_length=200, blank=True, null=True, default='')
    telcotransid = models.CharField(max_length=200, blank=True, null=True, default='')
    transactionid = models.CharField(max_length=200, blank=True, null=True, default='')
    reason = models.TextField(blank=True, null=True, default='')
    statusdate = models.CharField(max_length=200, blank=True, null=True, default='')
    
    def __str__(self):  
        return str(self.status or '')

class CardCallbacks(models.Model):
    status = models.CharField(max_length=200, blank=True, null=True, default='')
    reason = models.TextField(blank=True, null=True, default='')    
    transactionid = models.CharField(max_length=200, blank=True, null=True, default='')
    clienttransid = models.CharField(max_length=200, blank=True, null=True, default='')
    clientreference = models.CharField(max_length=200, blank=True, null=True, default='')
    statusdate = models.CharField(max_length=200, blank=True, null=True, default='')
    brandtransid = models.CharField(max_length=200, blank=True, null=True, default='')
    
    def __str__(self):  
        return str(self.status or '')

class CashoutCallbacks(models.Model):
    status = models.CharField(max_length=200, blank=True, null=True, default='')
    clienttransid = models.CharField(max_length=200, blank=True, null=True, default='')
    clientreference = models.CharField(max_length=200, blank=True, null=True, default='')
    telcotransid = models.CharField(max_length=200, blank=True, null=True, default='')
    transactionid = models.CharField(max_length=200, blank=True, null=True, default='')
    reason = models.TextField(blank=True, null=True, default='')
    statusdate = models.CharField(max_length=200, blank=True, null=True, default='')
    
    def __str__(self):  
        return str(self.status or '')

class MyBusinessPayPaymentCallbacks(models.Model):
    status = models.CharField(max_length=100, blank=True, null=True, default='')
    payment_date = models.CharField(max_length=100, blank=True, null=True, default='')
    reference = models.CharField(max_length=100, blank=True, null=True, default='')
    currency = models.CharField(max_length=100, blank=True, null=True, default='')
    status_code = models.CharField(max_length=100, blank=True, null=True, default='')
    charge = models.CharField(max_length=100, blank=True, null=True, default='')
    tokenized = models.CharField(max_length=100, blank=True, null=True, default='')
    source = models.TextField(blank=True, null=True, default='')
    source_object = models.CharField(max_length=100, blank=True, null=True, default='')
    source_type = models.CharField(max_length=100, blank=True, null=True, default='')
    source_number = models.CharField(max_length=100, blank=True, null=True, default='')
    source_reference = models.CharField(max_length=100, blank=True, null=True, default='')
    amount = models.CharField(max_length=100, blank=True, null=True, default='')
    transaction_uuid = models.CharField(max_length=100, blank=True, null=True, default='')
    amount_after_charge = models.CharField(max_length=100, blank=True, null=True, default='')
    message = models.CharField(max_length=100, blank=True, null=True, default='')
    processor_transaction_id = models.CharField(max_length=100, blank=True, null=True, default='')
    error_fields = models.CharField(max_length=100, blank=True, null=True, default='')
    metadata = models.TextField(blank=True, null=True, default='')
    metadata_order_id = models.CharField(max_length=100, blank=True, null=True, default='')
    metadata_product_description = models.CharField(max_length=100, blank=True, null=True, default='')
    datecreated = models.DateTimeField(default=timezone.now)

    def __str__(self):  
        return str(self.status or '')

class HubtelCallbacks(models.Model):
    message = models.CharField(max_length=200, blank=True, null=True, default='')
    responseCode = models.CharField(max_length=200, blank=True, null=True, default='')
    data = models.TextField(blank=True, null=True, default='')
    datecreated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):  
        return str(self.responseCode or '')






