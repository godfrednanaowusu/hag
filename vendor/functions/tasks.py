from django.shortcuts import render, Http404
from django.http import HttpResponse,  HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Min, Sum, Avg, Max, Q, F
import urllib, json
import time
import re
import requests
from requests.auth import HTTPBasicAuth
import math
import base64
from math import cos, asin, sqrt
from datetime import *
from time import gmtime, strftime
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.utils.http import urlencode
from django.urls import *
from hag.celery import app
# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
from accounts.models import *
from nominations.models import *
from votes.models import *
from decimal import Decimal, DecimalException

from django.utils.html import escape
import uuid

# #######################################
# ######### Functions ###############
# #######################################

@app.task
def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if params:
        url += '?' + urlencode(params)
    return url

@app.task
def placemessageontemplate(request, message):
    requestpath = 'https://www.humanitarianawardsglobal.com'
    logo = '/static/images/logo.png'
    name = 'Humanitarian Awards Global'
    location = 'P.O.Box WY 1914 Kwabenya Accra'
    phone = '+233 24 917 4715 | +233 24 465 6402'
    email = 'info@humanitarianawardsglobal.com'
    website = 'www.humanitarianawardsglobal.com'

    messageontemplate = '<div style="background:#f9f9f9; width:100%; height:auto; padding:20px; box-sizing:border-box; "><div style="overflow:hidden; font-family:arial; width:98%; max-width: 700px; margin:0 auto; font-size:100%; padding:10px;  box-sizing:border-box; -webkit-box-sizing:border-box; color:#616161;"> <div style="width:100%; border-radius: 4px; border: 1px solid #eee;"> <div id="head" style="background:#efefef; color:rgb(40, 57, 65); min-height: 70px; padding:5px 20px;  " > <img src="'+ logo +'" style="height:50px; width:auto; padding: 10px 10px; display:inline-block; vertical-align: middle;"> <div style="display:inline-block; font-size:90%; vertical-align: middle; padding:10px; "> <h2 style="margin:0;">'+ str(name) +'</h2>  <p style="margin:0; font-size:70%;"><b>Address:</b> '+ str(location)+'</p> <p style="margin:0; font-size:70%;"><b>Phone:</b> '+ str(phone)+' <b>Email:</b> '+ str(email) +' </p> <p style="margin:0; font-size:70%;"><b>Website:</b> '+ str(website) +' </p> </div>   </div> <div id="body" style="background-color:#fff; padding:30px 30px; color:rgb(27, 27, 27);">' + message +'</div>  <div id="foot" style="color:rgb(27, 27, 27); width:100%; padding:0px; font-size:80%; text-align:left;">  </div> </div>  <span style="color: #1abc9c; font-size: 70%; margin:5px 10px;">powered by <a href="www.humanitarianawardsglobal.com" style=" color: #1abc9c; text-decoration:none; ">www.humanitarianawardsglobal.com</a></span> </div></div>'
    return str(messageontemplate)

@app.task
def formatphonenumber(country, phonenumber):
    try:
        country = Countries.objects.filter(nicename=country).last()
        phonestring = ''
        try:
            phonestring = int(re.sub(r'\s+','',re.sub(r'\D','', phonenumber)))
        except Exception as e:
            return {'status': 'failed', 'value': 'Phonenumber Error: '+str(e)}
        
        if len(str(phonestring)) >= country.minimum_nsn and len(str(phonestring)) <= country.maximum_nsn:
            # return str(country.phonecode) + str(phonestring)
            return {'status': 'success', 'value': str(country.phonecode) + str(phonestring)}
        elif len(str(phonestring)) == len(str(country.phonecode))+int(country.minimum_nsn) or len(str(phonestring)) == len(str(country.phonecode))+int(country.maximum_nsn):
            # return phonestring
            return {'status': 'success', 'value': str(phonestring)}
        else:
            return {'status': 'failed', 'value': 'Invalid Phonenumber'}
            
    except Exception as e:
        return {'status': 'failed', 'value': 'Phonenumber Formatting Error'+str(e)}


# #######################################
# ######### End of Functions ###############
# #######################################


# #######################################
# ######### Payments ###############
# #######################################

class HAGPayment():
    
    # init method or constructor 
    def __init__(self, request): 
        ####### WIGAL ######    
        self.baseurl = 'https://www.humanitarianawardsglobal.com'
        self.wigal_url_ussd = 'https://api.reddeonline.com/v1/receive'
        self.wigal_url_card = 'https://api.reddeonline.com/v1/checkout'
        # wigal_url_ussd
        self.wigal_appid = '1097'
        self.wigal_apikey = 'aVbye3uswjLF8PJPaXMv8nUujYWqhYdq4AqM33QnKVpqFg76Qd'

        ####### MY BUSINESS PAY ######
        self.mybusinesspay_url = 'https://payment.asoriba.com/payment/v1.0/initialize'
        self.mybusinesspay_authorisation = 'Bearer PVWIthNN_bIbnjeLIDEUkeJvfJ2qnYQ1kb_O0XXyE2qpdT0n79l7zFgNOwrk'

        ####### SEERBIT ######
        self.seerbit_url = 'https://seerbitapi.com/api/v2/payments'
        self.seerbit_authorisation = 'Bearer PVWIthNN_bIbnjeLIDEUkeJvfJ2qnYQ1kb_O0XXyE2qpdT0n79l7zFgNOwrk'
        self.seerbit_publickey = ''

        ##### HUBTEL ######
        self.hubtel_url_card = 'https://payproxyapi.hubtel.com/items/initiate'
        
        # print(self.baseurl+reverse('payment-successful'))
        
    @app.task(bind=True, max_retries=3)
    def payment_initiate(self, paymenttype, nominee_code, votecount, amount, network, msisdn, trafficId, payer_fullname):  
        self.baseurl = 'https://www.humanitarianawardsglobal.com'
        self.wigal_url_ussd = 'https://api.reddeonline.com/v1/receive'
        self.wigal_url_card = 'https://api.reddeonline.com/v1/checkout'
        # wigal_url_ussd
        self.wigal_appid = '1097'
        self.wigal_apikey = 'aVbye3uswjLF8PJPaXMv8nUujYWqhYdq4AqM33QnKVpqFg76Qd'

        ####### MY BUSINESS PAY ######
        self.mybusinesspay_url = 'https://payment.asoriba.com/payment/v1.0/initialize'
        self.mybusinesspay_authorisation = 'Bearer PVWIthNN_bIbnjeLIDEUkeJvfJ2qnYQ1kb_O0XXyE2qpdT0n79l7zFgNOwrk'

        ####### SEERBIT ######
        self.seerbit_url = 'https://seerbitapi.com/api/v2/payments'
        self.seerbit_authorisation = 'Bearer PVWIthNN_bIbnjeLIDEUkeJvfJ2qnYQ1kb_O0XXyE2qpdT0n79l7zFgNOwrk'
        self.seerbit_publickey = ''

        ##### HUBTEL ######
        self.hubtel_url_card = 'https://payproxyapi.hubtel.com/items/initiate'
        
          
        # return JsonResponse({'status': 'success'})
        try:  
            if paymenttype == 'ussd':
                payment_processor = 'redde' # 'redde', 'mybusinesspay', 'paypal', 'hubtel'
            elif paymenttype == 'card':
                payment_processor = 'redde' # 'redde', 'mybusinesspay', 'paypal', 'hubtel'
            else:
                payment_processor = 'redde' # 'redde', 'mybusinesspay', 'paypal', 'hubtel'

            nominee = Nominations.objects.filter(nominee_code=nominee_code).last()
            if not nominee:	
                return JsonResponse({'status': 'failure', 'message':'Nominee Doesnt Exist'})
            paym_title = 'HAG Votes Payment'
            paym_description = 'Payment of '+str(votecount)+' vote(s) for '+str(nominee.nominee_firstname or '')+' '+str(nominee.nominee_lastname or '')+' at GHS'+str(amount)
            
            
            transId = str(uuid.uuid4())
            paym_request = PaymentRequests(payment_processor=payment_processor, paymenttype=paymenttype, clienttransid=transId, amount=amount, title=paym_title, description=paym_description, valuename='Votes', value=votecount, custom_code=nominee_code, payer_fullname='', payer_phonenumber=msisdn, payer_email='' )
            paym_request.save()
            # return JsonResponse({'status': 'failure', 'message':'Reached'})
            clientrefId = str(paym_request.clientrefid)
            

            # Process USSD
            if paymenttype == 'ussd':
                # via Redde
                if payment_processor == 'redde':
                    try:  
                        if msisdn.startswith('23324') or msisdn.startswith('23353') or msisdn.startswith('23354') or msisdn.startswith('23355') or msisdn.startswith('23359') or network == 'mtn_gh':
                            network = 'MTN'
                        elif msisdn.startswith('23327') or msisdn.startswith('23357') or msisdn.startswith('23326') or msisdn.startswith('23356') or network == 'tigo_gh' or network == 'airtel_gh':
                            network = 'AIRTELTIGO'
                        elif msisdn.startswith('23320') or msisdn.startswith('23350') or network == 'vodafone_gh':
                            network = 'VODAFONE'
                        else:
                            network = 'MTN'                            
                        
                        		
                        payload = { "amount": amount, "appid": "1437", "clientreference": clientrefId, "clienttransid": transId, "description": paym_description, "nickname": "HAG Voting", "paymentoption": network, "walletnumber": msisdn, "ussdtrafficid":trafficId }                
                        headers = {"Content-Type": "application/json;charset=UTF-8", "apikey": "6Z7sxBtWTxmCXBHmManB9NJwVk5dDjfFMendgKg3VfWVeaYZA9" }
                        # print(f'paym_description: {paym_description}')
                        # print(f'response: {paym_description}')
                        # return JsonResponse({'status': 'success'})
                        # print(f'payload: {json.dumps(payload)} - {timezone.now()}')
                        
                        response = requests.request('POST', 'https://api.reddeonline.com/v1/receive', data=json.dumps(payload), headers=headers)

                        # print(f'paym_description: {paym_description}')
                        # print(f'response: {response.content} - {timezone.now()}')
                        
                        d = json.loads(response.content)
                        if d['status'] == 'OK':
                            return JsonResponse({'status': 'success', 'network':network, 'message':d['reason']})
                        if d['status'] == 'FAILED':
                            return JsonResponse({'status': 'failure', 'message':d['reason']})
                        else:
                            return JsonResponse({'status': 'failure', 'message':'Payment Gateway Unreachable'})

                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})
                
                # via MyBusinessPay
                elif payment_processor == 'mybusinesspay':
                    try:  
                        if msisdn.startswith('23324') or msisdn.startswith('23354') or msisdn.startswith('23355') or msisdn.startswith('23359') or network == 'mtn_gh':
                            network = 'mtn_gh'
                        elif msisdn.startswith('23326') or msisdn.startswith('23356') or network == 'airtel_gh':
                            network = 'airtel_gh'
                        elif msisdn.startswith('23327') or msisdn.startswith('23357') or network == 'tigo_gh':
                            network = 'tigo_gh'
                        elif msisdn.startswith('23320') or msisdn.startswith('23350') or network == 'vodafone_gh':
                            network = 'vodafone_gh'
                        else:
                            network = 'mtn_gh'
                            
                        
                        payload = { 'amount':amount, 'metadata': { 'order_id':clientrefId, 'product_name':'HAG Votes Payment', 'product_description':paym_description }, 
                            'post_url':'https://www.humanitarianawardsglobal.com/mybusinesspay-payment-posturl/', 'currency':'GHS', 'order_image_url':'/static/images/logo.png',
                            'first_name': 'payer firstname', 'last_name': 'payer lastname', 'email': '', 'phone_number': str(msisdn), 'capture': True, 'payment_method':str(network)                    
                        }                
                        
                        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization':self.mybusinesspay_authorisation }
                        response = requests.request('POST', self.mybusinesspay_url, data=json.dumps(payload), headers=headers)
                        # return JsonResponse({'status': 'failure', 'message':str(response.text)})
                        # print(f'payload: {response.text}')
                        d = json.loads(str(response.text))
                        if d['status_code'] == 100:
                            return JsonResponse({'status': 'success', 'network':network, 'message':''})
                        else:
                            return JsonResponse({'status': 'failure', 'message':'Payment Failed'})

                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})

                # via Hubtel
                elif payment_processor == 'hubtel':
                    try:  
                        if msisdn.startswith('23324') or msisdn.startswith('23353') or msisdn.startswith('23354') or msisdn.startswith('23355') or msisdn.startswith('23359') or network == 'mtn_gh':
                            network = 'mtn-gh'
                        elif msisdn.startswith('23327') or msisdn.startswith('23357') or msisdn.startswith('23326') or msisdn.startswith('23356') or network == 'tigo_gh' or network == 'airtel_gh':
                            network = 'tigo-gh'
                        elif msisdn.startswith('23320') or msisdn.startswith('23350') or network == 'vodafone_gh':
                            network = 'vodafone-gh'
                        else:
                            network = 'mtn-gh'
                        		
                        payload = { 
                            "CustomerName": "",
                            "CustomerMsisdn": msisdn,
                            "CustomerEmail": "",
                            "Channel": network,
                            "Amount": amount,
                            "PrimaryCallbackUrl": 'https://www.humanitarianawardsglobal.com/hubtel-ussd-callback/', # self.baseurl+reverse("hubtel_ussd_callback"), #"https://webhook.site/98af9e87-03e7-4ee7-9596-825419009267", # self.baseurl+reverse("hubtel_ussd_callback"),
                            "Description": paym_description,
                            "ClientReference": transId
                            }      
                        # print(f'sample payload: {payload}')
                        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Basic WVFxUDVKMjozZDdkOTk2ZWJhYmQ0MTIxODYxMWI4MzJkMDFkNGFmMQ==' }
                        # print(f'sample headers: {headers}')
                        response = requests.request('POST', 'https://rmp.hubtel.com/merchantaccount/merchants/2017716/receive/mobilemoney', data=json.dumps(payload), headers=headers)
                        d = json.loads(response.content)
                        print(f'response: {d}')
                        if d['ResponseCode'] == '0001':
                            return JsonResponse({'status': 'success', 'network':network, 'message':d['Message']})
                        else:
                            return JsonResponse({'status': 'failure', 'message':d['Message']})
                        
                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})
                
            elif paymenttype == 'card':
                # via Redde
                if payment_processor == 'redde':
                    try:  
                        paym_request.clienttransid = transId
                        paym_request.save()	
                        payload = { "apikey": "aVbye3uswjLF8PJPaXMv8nUujYWqhYdq4AqM33QnKVpqFg76Qd", "appid": "1097", "amount": amount, "description": paym_description, "logolink":"https://humanitarianawardsglobal.com/static/images/logo.png", "merchantname":"Humanitarian Awards Global", "clienttransid": transId, "successcallback":"https://www.humanitarianawardsglobal.com/payment-successful", "failurecallback":"https://www.humanitarianawardsglobal.com/payment-failed"}               
                        headers = {'Content-Type': 'application/json;charset=UTF-8', 'apikey': 'aVbye3uswjLF8PJPaXMv8nUujYWqhYdq4AqM33QnKVpqFg76Qd' }
                        response = requests.request('POST', 'https://api.reddeonline.com/v1/checkout', data=json.dumps(payload), headers=headers)
                        d = json.loads(response.content)
                        # return JsonResponse({'status': 'failure', 'message': d})
                        if d['status'] == 'OK':
                            return JsonResponse({'status': 'success', 'link':d['checkouturl']})
                        else:
                            return JsonResponse({'status': 'failure', 'message':d['message']})
                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})
                
                # via MyBusinessPay
                elif payment_processor == 'mybusinesspay':
                    try:  
                        payload = { 'amount':amount, 'metadata': { 'order_id':clientrefId, 'product_name':'HAG Votes Payment', 'product_description':paym_description }, 
                            'callback':self.baseurl+reverse('mybusinesspay_payment_callback'), 'post_url':self.baseurl+reverse('mybusinesspay_payment_posturl'), 'currency':'GHS', 'order_image_url':'/static/images/logo.png',
                            'first_name': '', 'last_name': '', 'email': '', 'phone_number': str(msisdn), 'capture': False, 'payment_method':str(network)                    
                        }                
                        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization':self.mybusinesspay_authorisation }
                        response = requests.request('POST', self.mybusinesspay_url, data=json.dumps(payload), headers=headers)
                        d = json.loads(str(response.text))
                        # return JsonResponse({'status': 'failure', 'message':str(response.text)})
                        if d['status_code'] == '100' and d['status'] == 'success':
                            return JsonResponse({'status': 'success', 'link':d['url'], 'message':''})
                        else:
                            return JsonResponse({'status': 'failure', 'message':'Payment Failed'})

                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})
                
                # via Seerbit
                elif payment_processor == 'seerbit':
                    try:  
                        payload = { 'publicKey':self.seerbit_publickey, 'amount':amount, 'currency':'', 'country':'', 'paymentReference':clientrefId, 'metadata': { 'order_id':clientrefId, 'product_name':'HAG Votes Payment', 'product_description':paym_description }, 
                            'callback':self.baseurl+reverse('mybusinesspay_payment_callback'), 'post_url':self.baseurl+reverse('mybusinesspay_payment_posturl'), 'currency':'GHS', 'order_image_url':'/static/images/logo.png',
                            'first_name': '', 'last_name': '', 'email': '', 'phone_number': str(msisdn), 'capture': False, 'payment_method':str(network)                    
                        }                
                        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization':self.mybusinesspay_authorisation }
                        response = requests.request('POST', self.mybusinesspay_url, data=json.dumps(payload), headers=headers)
                        d = json.loads(str(response.text))
                        # return JsonResponse({'status': 'failure', 'message':str(response.text)})
                        if d['status_code'] == '100' and d['status'] == 'success':
                            return JsonResponse({'status': 'success', 'link':d['url']})
                        else:
                            return JsonResponse({'status': 'failure', 'message':'Payment Failed'})

                    except Exception as e:   
                        return JsonResponse({'status': 'failure', 'message':str(e)})

                # via Hubtel
                elif payment_processor == 'hubtel':
                    try:  
                        paym_request.clienttransid = transId
                        paym_request.save()	
                        # payload = { 
                        #     'totalAmount': amount, 
                        #     'description': paym_description,
                        #     'callbackUrl':self.baseurl+reverse('hubtel_ussd_callback'),
                        #     'returnUrl':self.baseurl+reverse('hubtel_return_callback'),
                        #     "merchantAccountNumber": "2017716",
                        #     "cancellationUrl": self.baseurl+reverse('hubtel_cancel_callback'),
                        #     "clientReference": transId
                        #     }  
                        payload = {
                            "totalAmount": amount,
                            "description": paym_description,
                            "callbackUrl": self.baseurl+reverse('hubtel_ussd_callback'),
                            "returnUrl": self.baseurl+reverse('hubtel_return_callback'),
                            "merchantAccountNumber": "2017716",
                            "cancellationUrl": self.baseurl+reverse('hubtel_cancel_callback'),
                            "PayeeMobileNumber": msisdn,
                            "PayeeName": payer_fullname,
                            "PayeeEmail": "",
                            "clientReference": transId
                        }      
                        # print(f'payload: {payload}')        
                        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'Basic WVFxUDVKMjozZDdkOTk2ZWJhYmQ0MTIxODYxMWI4MzJkMDFkNGFmMQ==' }
                        response = requests.request('POST', self.hubtel_url_card, data=json.dumps(payload), headers=headers)
                        # print(f'console: {response.content}')
                        d = json.loads(response.content)
                        if d['responseCode'] == '0000' and d['status'] == 'Success':
                            return JsonResponse({'status': 'success', 'link':d['data']['checkoutUrl']})
                        else:
                            return JsonResponse({'status': 'failure', 'message':d['data']['message']})
                    except Exception as e:   
                        print(f'hubtel checkout error: {e}')
                        return JsonResponse({'status': 'failure', 'message':str(e)})
                
            elif payment_processor == 'paypal':
                pass
            
            else:
                pass

            return JsonResponse({'status': 'success'})
        except Exception as e:   
            return JsonResponse({'status': 'failure', 'message':str(e)})

    
############# USSD PAYMENTS ##############
@app.task
def hag_ussd_payment_initiate(nominee_code, votecount, amount, network, msisdn):    
    try:  
        nominee = Nominations.objects.filter(nominee_code=nominee_code).last()	
        paym_processor = 'Redde' # MyBusinessPay', 'Paypal'
        paym_type = 'USSD' # 'Card', 'Paypal'
        paym_title = 'HAG Votes Payment'
        paym_description = 'Payment of '+str(votecount)+' votes for '+str(nominee.nominee_firstname)+' '+str(nominee.nominee_lastname)+' at GHS'+amount
        paym_request = PaymentRequests(payment_processor=paym_processor, paymenttype=paym_type, amount=amount, title=paym_title, description=paym_description, valuename='Votes', value=votecount, custom_code=nominee_code, payer_fullname='', payer_phonenumber=msisdn, payer_email='' )
        paym_request.save()

        wigal_ussd_payment_initiate(paym_request.refid, nominee_code, votecount, amount, network, msisdn, paym_title, paym_description)
        # mybusinesspay_ussd_payment_initiate(paym_request.refid, nominee_code, votecount, amount, network, msisdn, paym_title, paym_description)

        return 'success'

    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})

@app.task
def wigal_ussd_payment_initiate(clientrefId, nominee_code, votecount, amount, network, msisdn, title, description):    
    try:  
        if msisdn.startswith('23324') or msisdn.startswith('23354') or msisdn.startswith('23355') or msisdn.startswith('23359'):
            network = 'MTN'
        elif msisdn.startswith('23327') or msisdn.startswith('23357') or msisdn.startswith('23326') or msisdn.startswith('23356'):
            network = 'AIRTELTIGO'
        elif msisdn.startswith('23320') or msisdn.startswith('23350'):
            network = 'VODAFONE'
        else:
            network = 'MTN'

        transId = str(uuid.uuid4())		
        baseurl = 'https://api.reddeonline.com/v1/receive'              
        payload = {
            "amount": amount,
            "appid": "1097",
            "clientreference": clientrefId,
            "clienttransid": transId,
            "description": description,
            "nickname": "HAG",
            "paymentoption": network, #(MTN | AIRTELTIGO | VODAFONE)
            "walletnumber": msisdn
        }                
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'apikey': 'aVbye3uswjLF8PJPaXMv8nUujYWqhYdq4AqM33QnKVpqFg76Qd' }
        response = requests.request("POST", baseurl, data=json.dumps(payload), headers=headers)
        return response.json()
    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})

@app.task
def mybusinesspay_ussd_payment_initiate(clientrefId, nominee_code, votecount, amount, network, msisdn, title, description):    
    try:  
        nominee = Nominations.objects.filter(nominee_code=nominee_code).last()	
        baseurl = 'https://payment.asoriba.com/payment/v1.0/initialize'              
        payload = {
            "amount":amount, 
            "metadata": 
            {
                "order_id":clientrefId, 
                "product_name":"HAG Votes Payment", 
                "product_description":'Payment of '+str(votecount)+' votes for '+str(nominee.nominee_firstname)+' '+str(nominee.nominee_lastname)+' at GHS'+amount
            }, 
            "callback":'https://www.humanitarianawardsglobal.com'+reverse('hag_online_payment_callback'), 
            "currency":"GHS", 
            "order_image_url":"/static/images/logo.png",
            "first_name": "Payer Firstname",         
            "last_name": "Payer Lastname",
            "email": "Payer Email Address",
            "phone_number": str(msisdn),
            "capture": True,
            "payment_method":str(network)                    
        }                
        headers = {'Accept': "application/json", 'Content-Type': "application/json", "Authorization":"Bearer FMJ8BWTMRMF6xHPjediLo5Le9PWnzo4Yt8tN20xEb07Rsrp9--_rhLJeKs4V" }
        response = requests.request("POST", baseurl, data=json.dumps(payload), headers=headers)
        return response.text
    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})

############# END USSD PAYMENTS ##############

############# USSD PAYMENTS ##############
@app.task
def hag_card_payment_initiate(nominee_code, votecount, amount):    
    try:  
        nominee = Nominations.objects.filter(nominee_code=nominee_code).last()	
        paym_processor = 'Redde' # MyBusinessPay', 'Paypal'
        paym_type = 'USSD' # 'Card', 'Paypal'
        paym_title = 'HAG Votes Payment'
        paym_description = 'Payment of '+str(votecount)+' votes for '+str(nominee.nominee_firstname)+' '+str(nominee.nominee_lastname)+' at GHS'+amount
        paym_request = PaymentRequests(payment_processor=paym_processor, paymenttype=paym_type, amount=amount, title=paym_title, description=paym_description, valuename='Votes', value=votecount, custom_code=nominee_code, payer_fullname='', payer_phonenumber=msisdn, payer_email='' )
        paym_request.save()

        wigal_ussd_payment_initiate(paym_request.refid, nominee_code, votecount, amount, network, msisdn, paym_title, paym_description)
        # mybusinesspay_ussd_payment_initiate(paym_request.refid, nominee_code, votecount, amount, network, msisdn, paym_title, paym_description)

        return 'success'

    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})


@app.task
def asoriba_card_payment_initiate(nominee_code, votecount, amount):    
    try:  
        orderid = str(uuid.uuid4())	
        nominee = Nominations.objects.filter(nominee_code=nominee_code).last()		
        baseurl = 'https://payment.asoriba.com/payment/v1.0/initialize'              
        payload = {
            "amount":amount, 
            "metadata": 
            {
                "order_id":orderid, 
                "product_name":"HAG Votes Payment", 
                "product_description":'Payment of '+str(votecount)+' votes for '+str(nominee.nominee_firstname)+' '+str(nominee.nominee_lastname)+' at GHS'+amount 
            }, 
            "callback":'https://www.humanitarianawardsglobal.com'+reverse('hag_online_payment_callback'), 
            "currency":"GHS", 
           "first_name": "Payer Firstname",         
            "last_name": "Payer Lastname",
            "email": "Payer Email Address",                  
        }                
        headers = {'Accept': "application/json", 'Content-Type': "application/json", "Authorization":"Bearer FMJ8BWTMRMF6xHPjediLo5Le9PWnzo4Yt8tN20xEb07Rsrp9--_rhLJeKs4V" }
        response = requests.request("POST", baseurl, data=json.dumps(payload), headers=headers)
        return response.text
    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})

# For Land Title App
@app.task
def asoribaland_ussd_payment_initiate(amount, phonenumber):    
    try:  
        orderid = str(uuid.uuid4())			
        baseurl = 'https://payment.asoriba.com/payment/v1.0/initialize'              
        payload = {
            "amount":amount, 
            "metadata": 
            {
                "order_id":orderid, 
                "product_name":"Land Title Verification", 
                "product_description":"Payment for Land Title Verification" 
            }, 
            "callback":'https://www.humanitarianawardsglobal.com/'+reverse('asoribaland_payment_successful'), 
            "currency":"GHS", 
            "first_name": "Land",         
            "last_name": "Veri",
            "email": "landverifi@gmail.com",
            "phone_number": phonenumber,
            "capture": True,
            "payment_method":"mtn_gh"                    
        }                
        headers = {'Accept': "application/json", 'Content-Type': "application/json", "Authorization":"Bearer FMJ8BWTMRMF6xHPjediLo5Le9PWnzo4Yt8tN20xEb07Rsrp9--_rhLJeKs4V" }
        response = requests.request("POST", baseurl, data=json.dumps(payload), headers=headers)
        return response.text
    except Exception as e:   
        return JsonResponse({'status': 'failure', 'message':str(e)})


class PaypalPayment():
    baseurl = ''
    
    ####### LIVE ######
    paypal_url = "https://api.paypal.com"
    paypal_clientid = 'AaGoGksaRFFsWkk5mHh1QNZq_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' 
    paypal_secretkey = 'EEwkpQGhzQhPGXHUE2kNqL-BlxuXOGtPq234gwBnoVMda-0mK9va0bDOXX0oKbVhphBQfwto10yVFFTN'

    ####### SANDBOX #######
    # paypal_url = "https://api.sandbox.paypal.com"  
    # paypal_clientid = 'AeLGpuSE6MqGT6yuRlaI6RJGJJdtIL7TrS5kk9N8IO0cIWeuOTLUdfsDEX_GOB77Rl5A65-lFmnVg5l-' 
    # paypal_secretkey = 'EHMJB2EMUqQlEy26L7Avc3M9Mdl9cPBgNBeHRAnW5nfj65iGV67qKHgei-Y9ZXIKdXdUCqtyShA4bKva'
    
    # init method or constructor 
    def __init__(self, request): 
        # baseurl = request.scheme + '://' + request.get_host() 
        baseurl = 'https://www.humanitarianawardsglobal.com'
        
    # @app.task
    def paypal_payment_getaccesstoken(self, request):	
        try:
            payload = { 'grant_type':'client_credentials' }
            userpass = self.paypal_clientid+':'+self.paypal_secretkey
            basicauth = base64.b64encode(userpass.encode("ascii")).decode("ascii")        
            headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic '+basicauth }
            response = requests.request("POST", self.paypal_url+'/v1/oauth2/token', data=payload, headers=headers)
            return response.json()
        except Exception as e:     
            return JsonResponse({'status': 'failure', 'message':str(e)})

    # @app.task
    def paypal_payment_initiate(self, request, amount, clientrefId, paymenttype):    
        try:  
            # baseurl = request.scheme + '://' + request.get_host()
            baseurl = 'https://www.humanitarianawardsglobal.com'
            paypal_gettoken = self.paypal_payment_getaccesstoken(request)   
            paypal_AccessToken = paypal_gettoken['access_token']                
            payload = {
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": baseurl+"/paypalpaymentredirect/",
                    "cancel_url": baseurl+"/paypalpaymentcancel/",
                    "brand_name": "HAG",
                    "locale": "en-US",
                    "landing_page": "BILLING",
                    "user_action": "CONTINUE"
                },
                "purchase_units": [
                    {
                        "reference_id": clientrefId,
                        "description": "HAG "+paymenttype+ " Payment",
                        "amount": {
                            "currency_code": "USD",
                            "value": amount
                        }
                    }
                ],
                "redirect_urls":{
                    "return_url":baseurl+"/paypalpaymentredirect/",
                    "cancel_url":baseurl+"/paypalpaymentcancel/"
                },
                "metadata":
                {
                    "payment_clientrefid": clientrefId,
                    "postback_data": []
                },
            }                
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ paypal_AccessToken }
            response = requests.request("POST", self.paypal_url+'/v2/checkout/orders', data=json.dumps(payload), headers=headers)
            return response.json()
        except Exception as e:   
            return JsonResponse({'status': 'failure', 'message':str(e)})

    def paypal_payment_authorize(self, request, token):    
        try:  
            paypal_gettoken = self.paypal_payment_getaccesstoken(request)   
            paypal_AccessToken = paypal_gettoken['access_token'] 
            payload = {}
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ paypal_AccessToken }
            response = requests.request("POST", self.paypal_url+'/v2/checkout/orders/'+token+'/capture', data=payload, headers=headers)
            return response.json()
        except Exception as e:   
            return JsonResponse({'status': 'failure', 'message':str(e)})

    def paypal_payment_retry(self, request, token):    
        try:  
            paypal_gettoken = self.paypal_payment_getaccesstoken(request)   
            paypal_AccessToken = paypal_gettoken['access_token'] 
            payload = {}
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+ paypal_AccessToken }
            response = requests.request("POST", self.paypal_url+'/checkoutnow?token'+token, data=payload, headers=headers)
            return response.json()
        except Exception as e:   
            return JsonResponse({'status': 'failure', 'message':str(e)})

# #######################################
# ######### End of Payments ###############
# #######################################

