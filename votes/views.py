from django.shortcuts import render, Http404
from django.template import RequestContext
from django.http import HttpResponse,  HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
import urllib, json
import time
from datetime import date, timedelta
import math
import random
from urllib.parse import urlparse
from os.path import splitext
# from django.contrib.gis.utils import GeoIP
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Min, Sum, Avg, Max, Q
from django.conf import settings
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import *
from django.views import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import *
from django.core.paginator import *
from django.utils import translation
from vendor.functions.tasks import *
import uuid
from decimal import Decimal, DecimalException

from .models import *

class VotesUSSDView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(VotesUSSDView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        network = str(request.GET.get('network') or '')
        sessionid = str(request.GET.get('sessionid') or '')
        mode = str(request.GET.get('mode') or '')
        msisdn = str(request.GET.get('msisdn') or '')
        userdata = str(request.GET.get('userdata') or '')
        username = str(request.GET.get('username') or '')
        trafficid = str(request.GET.get('trafficid') or '')
        other = str(request.GET.get('other') or '')
        awardscheme = AwardSchemes.objects.filter(latest=True).order_by('-id').last()
        vote_sess = VoteSessions.objects.filter(network=network, msisdn=msisdn, session_id=sessionid).last()
        nominee = VoteSessions.objects.filter(network=network, msisdn=msisdn, session_id=sessionid).exclude(nominee_code='').last()

        welcome_msg = 'Welcome to '+str(awardscheme.name or '')+'^^1. Vote for a Nominee^2. Learn More about '+str(awardscheme.name or '')
        enter_nom_code = 'Enter the Voting Code of the Nominee'
        visit_hag = 'Kindly visit www.humanitarianawardsglobal.com'
        nom_code = ''
        session_step = ''
        other_msg = ''

        response_msg = ''

        if userdata == '800*1111':            
            response_msg = welcome_msg
            session_step = '0'
            other_msg = 'hag'
            mode = 'more'       
        
        elif mode == 'more':                   
            if vote_sess:
                other_msg = vote_sess.other
                if vote_sess.session_step == '0':
                    if userdata == '1':
                        # # Covid 19 Message
                        # response_msg = 'Voting is currently on hold and would resume after the LOCKDOWN in Ghana, HAG urges you to stay home and stay safe.^^This too shall pass.'
                        # session_step = '01'
                        # mode = 'end'
                        response_msg = enter_nom_code
                        session_step = '01'
                    elif userdata == '2':
                        response_msg = visit_hag
                        session_step = '02'
                        mode = 'end'
                    else:
                        response_msg = 'Invalid Input, accepted inputs are 1 and 2'
                        session_step = '0'
                
                elif vote_sess.session_step == '01':
                    if userdata == '2':
                        response_msg = enter_nom_code
                        session_step = '01'
                    else:
                        nom_code = userdata
                        nomination = Nominations.objects.filter(category__scheme=awardscheme, nominee_code=nom_code).last()
                        if nomination:
                            vote_nominee = 'Do you want to vote for '+str(nomination.nominee_firstname or '') + ' '+str(nomination.nominee_lastname or '')+' to win ' + str(nomination.category.name or '')+'. ' +'^1. Confirm and Proceed to Payments^2. Back'
                            response_msg = vote_nominee
                            session_step = '011'
                        else:
                            response_msg = 'A Nominee with this voting code does not exist, Retry ^^' + enter_nom_code
                            session_step = '01'
                
                elif vote_sess.session_step == '011':
                    if userdata == '1':                            
                        response_msg = 'How many votes would you like to cast.^Enter numbers only.^^A vote costs GHS 1.00'
                        session_step = '0111'
                        mode = 'more'
                    elif userdata == '2':
                        response_msg = enter_nom_code
                        session_step = '011'
                    else:
                        response_msg = 'Invalid Input, accepted inputs are 1 and 2'
                        session_step = '011'

                elif vote_sess.session_step == '0111':
                    noofvotes = userdata
                    if noofvotes.isdigit():
                        calc_amount = str(round(float(noofvotes) * 1, 2))
                                                    
                        hag_payment = HAGPayment(request)	
                        # print(f'trafficid: {trafficid}')	
                        	
                        try:
                            hag_payment_response = hag_payment.payment_initiate.s(paymenttype='ussd', nominee_code=nominee.nominee_code, votecount=noofvotes, amount=calc_amount, network=vote_sess.network, msisdn=msisdn, trafficId=trafficid, payer_fullname='').apply_async(countdown=1)
                            print(f'response: {hag_payment_response}')
                            # hag_payment.payment_initiate(paymenttype='ussd', nominee_code=nominee.nominee_code, votecount=noofvotes, amount=calc_amount, network=vote_sess.network, msisdn=msisdn, trafficId=trafficid, payer_fullname='')
                        except Exception as e:
                            print(f'payment initiate error:- {timezone.now()}')
                            pass
                        
                        # print(f'paymentresponse:- {timezone.now()}')
                        if vote_sess.network == 'MTN' or vote_sess.network == 'mtn_gh':
                            response_msg = f'Wait for the prompt to finalize voting.^If not, check MoMo My Approvals.^^Thank you.'
                        else:
                            response_msg = f'Please wait for the payment prompt to finalize your voting.^^Thank you.'
                        session_step = '0111'
                        mode = 'end'
                        
                        request.session.flush()
                        
                        # if paymentresponse:
                        #     # return HttpResponse(paymentresponse.content)
                        #     d = json.loads(paymentresponse.content)
                        #     if d['status'] == 'success':
                        #         if d['network'] == 'MTN' or d['network'] == 'mtn_gh':
                        #             response_msg = f'Wait for the prompt to finalize voting.^If not, check MoMo My Approvals.^{d["message"]}'
                        #         else:
                        #             response_msg = f'Please wait for the payment prompt to finalize your voting.^^{d["message"]}^^Thank you.'
                        #         session_step = '0111'
                        #         mode = 'end'
                        #     else:
                        #         response_msg = 'Payment Initialization Error caused by: '+ str(d['message'])
                        #         session_step = '0111'
                        #         mode = 'end'
                        # else:
                        #     response_msg = 'Could not Initiate Payment at this time. Try Again'
                        #     session_step = '0111'
                        #     mode = 'end'

                    else:
                        response_msg = 'You didnt enter numbers only.^^ How many votes would you like to cast.^Enter numbers only.^^A vote costs GHS 1.00'
                        session_step = '011'
                        mode = 'more'
                    
                else:
                    response_msg = 'Cant go beyond this stage'

        elif mode == 'end':
            response_msg = ''

        if (network != '') and (sessionid != '') and (mode != '') and (msisdn != '') and (username != '') and (trafficid != ''):
            vote_session = VoteSessions(network=network, session_id=sessionid, mode=mode, msisdn=msisdn, userdata=userdata, response_to_user=response_msg, trafficid=trafficid, other=other_msg, nominee_code=nom_code, session_step=session_step )
            vote_session.save()

        response = network+'|'+mode+'|'+msisdn+'|'+sessionid+'|'+response_msg+'|'+username+'|'+trafficid+'|'+other_msg
        return HttpResponse(response, content_type="text/plain; charset=utf-8")
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        network = str(request.GET.get('network') or '')
        sessionid = str(request.GET.get('sessionid') or '')
        mode = str(request.GET.get('mode') or '')
        msisdn = str(request.GET.get('msisdn') or '')
        userdata = str(request.GET.get('userdata') or '')
        username = str(request.GET.get('username') or '')
        trafficid = str(request.GET.get('trafficid') or '')
        other = str(request.GET.get('other') or 'hag_menu')

        return HttpResponseRedirect(build_url('votes_ussd', kwargs={ }, params={'network':network, 'sessionid':sessionid, 'mode':mode, 'msisdn':msisdn, 'userdata':userdata, 'username':username, 'trafficid':trafficid, 'other':other	}))

class VotesOnlineView(View):
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        code = str(request.GET.get('code') or '')
        votecount = str(request.GET.get('votecount') or '')
        paymenttype = str(request.GET.get('paymenttype') or '')
        network = str(request.GET.get('network') or '')        
        msisdn = str(request.GET.get('msisdn') or '')
        payer_fullname = str(request.GET.get('payer_fullname') or '')
        trafficid = ''
        formattedphone = ''
        phoneformat_check = formatphonenumber('Ghana', msisdn)
        if phoneformat_check['status'] == 'success':       
            formattedphone = phoneformat_check['value']        

        # Calculation for Votes Cost
        if votecount:
            votecost = round(float(votecount) * 1.00, 2)
        else:
            messages.error(request, 'Vote Count was not found') 
            return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))       
        
        nominee = Nominations.objects.filter(nominee_code=code).last()
        if not nominee:
            messages.error(request, 'Nominee is Unavailable')
            return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))
        elif not votecount:
            messages.error(request, 'Vote Count was not found')
            return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))
        elif not votecost:
            messages.error(request, 'Vote Cost could not be calculated')
            return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))
        elif paymenttype == 'ussd' and (not formattedphone):
            messages.error(request, 'Phonenumber is not present')
            return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))
        else:
            hag_payment = HAGPayment(request)		
            
            paymentresponse = hag_payment.payment_initiate(paymenttype=paymenttype, nominee_code=nominee.nominee_code, votecount=votecount, amount=votecost, network=network, msisdn=formattedphone, trafficId=trafficid, payer_fullname=payer_fullname)
            if paymentresponse:
                # return HttpResponse(paymentresponse.content)
                d = json.loads(paymentresponse.content)                
                if d['status'] == 'success':                    
                    if paymenttype == 'ussd':
                        if network == 'mtn_gh':
                            messages.success(request, f'Payment Initiated Successfully, {d["message"]}, you should receive a prompt soon. In a case the prompt doesnt show, kindly dial *170#, then 6. My Wallet then 3. My Approvals to complete the payment make sure you have enough balance')
                        else:
                            messages.success(request, f'Payment Initiated Successfully, {d["message"]}, you should receive a prompt soon, make sure you have enough balance')
                    elif paymenttype == 'card':
                        return HttpResponseRedirect(d['link'])
                    else:
                        messages.success(request, 'Unidentified Payment Type')
                else:
                    messages.error(request, 'Payment could not be initiated due to '+d['message'])        
        
        return HttpResponseRedirect(build_url('vote', kwargs={ }, params={'code':code }))
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        code =f"{request.POST.get('code') or request.GET.get('code') }"
        votecount =f"{request.POST.get('votecount') or request.GET.get('votecount') }"
        paymenttype =f"{request.POST.get('paymenttype') or request.GET.get('paymenttype') }"
        network =f"{request.POST.get('network') or request.GET.get('network') }'       "
        msisdn =f"{request.POST.get('msisdn') or request.GET.get('msisdn') }"
        payer_fullname =f"{request.POST.get('payer_fullname') or request.GET.get('payer_fullname') }"
        
        return HttpResponseRedirect(build_url('votes_online', kwargs={ }, params={'code':code, 'votecount':votecount, 'paymenttype':paymenttype, 'network':network, 'msisdn':msisdn, 'payer_fullname':payer_fullname	}))

########### Wigal Callbacks #############
# Wigal Callbacks
class WigalCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WigalCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('Wigal Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4            
            # print(f'Wigal Callback Payload: {json_data}')
            status = json_data.get('status', {})
            clienttransid = json_data.get('clienttransid', {})
            clientreference = json_data.get('clientreference', {})
            transactionid = json_data.get('transactionid', {})
            reason = json_data.get('reason', {})
            statusdate = json_data.get('statusdate', {})
            telcotransid = json_data.get('telcotransid', {})
            brandtransid = json_data.get('brandtransid', {})
            
            callback = WigalCallbacks(status=status, reason=reason, transactionid=transactionid, clienttransid=clienttransid, clientreference=clientreference, telcotransid=telcotransid, brandtransid=brandtransid, statusdate=statusdate)
            callback.save()

            if status == 'PAID':    
                updatevotes('redde', clienttransid, transactionid)


            # if telcotransid:
            #     callback = USSDCallbacks(status=status, clienttransid=clienttransid, clientreference=clientreference, telcotransid=telcotransid, transactionid=transactionid, reason=reason, statusdate=statusdate)
            #     callback.save()
            # else:
            #     callback = CardCallbacks(status=status, reason=reason, transactionid=transactionid, clienttransid=clienttransid, clientreference=clientreference, statusdate=statusdate)
            #     callback.save()

            # if status == 'PAID':    
            #     if telcotransid:            
            #         response = updatevotes_viaussd(clientreference, clienttransid, transactionid)
            #     else:
            #         response = updatevotes_viacard(clienttransid, transactionid)

            #     if response == 'success':
            #         return HttpResponse('Payment Callback Succeeded')
            # elif status == 'FAILED':
            #     return HttpResponse('Payment Callback Failed')
            else:
                return HttpResponse('Payment Callback Error')
        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('Wigal Callback Reached')

class WigalCardSuccessfulCallbackView(View):
    form_class = ''
    initial = {'': ''}
    template_wigal_payment_successful = 'wigal_payment_successful.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_wigal_payment_successful, {  })

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

class WigalCardFailureCallbackView(View):
    form_class = ''
    initial = {'': ''}
    template_wigal_payment_failed = 'wigal_payment_failed.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_wigal_payment_failed, {  })

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

class WigalCashoutCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WigalCashoutCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('Wigal Cashout Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4  

            status = json_data.get('status', {})
            clienttransid = json_data.get('clienttransid', {})
            clientreference = json_data.get('clientreference', {})
            telcotransid = json_data.get('telcotransid', {})
            transactionid = json_data.get('transactionid', {})
            reason = json_data.get('reason', {})
            statusdate = json_data.get('statusdate', {})

            callback = CashoutCallbacks(status=status, clienttransid=clienttransid, clientreference=clientreference, telcotransid=telcotransid, transactionid=transactionid, reason=reason, statusdate=statusdate)
            callback.save()

            if status == 'PAID':                
                return HttpResponse('Cashout Callback Succeeded')
            elif status == 'FAILED':
                return HttpResponse('Cashout Callback Failed')
            else:
                return HttpResponse('Cashout Callback Error')

        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('Wigal Cashout Callback Reached')

########### Wigal Callbacks #############


########### MyBusinessPay Callbacks #############
# MyBusinessPay Callbacks
class MyBusinessPayPaymentCallbackView(View):    
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        try:
            amount = request.GET.get('amount')
            amount_after_charge = request.GET.get('amount_after_charge')
            charge = request.GET.get('charge')
            currency = request.GET.get('currency')
            customer_remarks = request.GET.get('customer_remarks')
            email = request.GET.get('email')
            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')
            message = request.GET.get('message')
            metadata_order_id = request.GET.get('metadata[order_id]')
            metadata_product_description = request.GET.get('metadata[product_description]')
            metadata_product_name = request.GET.get('metadata[product_name]')
            payment_date = request.GET.get('payment_date')
            processor_transaction_id = request.GET.get('processor_transaction_id')
            # processor_transaction_id = ''
            reference = request.GET.get('reference')
            source_object = request.GET.get('source[object]')
            source_number = request.GET.get('source[number]')
            source_reference = request.GET.get('source[reference]')
            source_type = request.GET.get('source[type]')
            status = request.GET.get('status')
            status_code = request.GET.get('status_code')
            tokenized = request.GET.get('tokenized')
            transaction_uuid = request.GET.get('transaction_uuid')
            
            
            callback = MyBusinessPayPaymentCallbacks(status=status, payment_date=payment_date, reference=reference, currency=currency, status_code=status_code, charge=charge, tokenized=tokenized, source_object=source_object, source_type=source_type, source_number=source_number, source_reference=source_reference, amount=amount, transaction_uuid=transaction_uuid, amount_after_charge=amount_after_charge, message=message, processor_transaction_id=processor_transaction_id, metadata_order_id=metadata_order_id, metadata_product_description=metadata_product_description)
            callback.save()

            if status.lower() == 'successful':   
                messages.success(request, 'Thank you for using HAG, Voting was successful')
                return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))
            elif status.lower() == 'cancelled':   
                messages.success(request, 'Payment was Cancelled')
                return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))
            elif status.lower() == 'failed':   
                messages.success(request, 'Transaction Failed because '+str(message))
                return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))
            else:
                messages.success(request, 'There was an issue because '+str(message))
                return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))
                    
            
        except Exception as e:
            messages.success(request, 'Error because '+str(e))
            return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))

        messages.success(request, 'HAG Voting Service')
        return HttpResponseRedirect(build_url('mybusinesspay_payment_thankyou', kwargs={ }, params={ }))
        
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

class MyBusinessPayPaymentThankYouView(View):
    form_class = ''
    initial = {'': ''}
    template_payment_thanks = 'payment_thanks.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_payment_thanks, {  })

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

class MyBusinessPayPaymentPostURLView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MyBusinessPayPaymentPostURLView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('HAG is expecting a POST response here not GET, try POST')
        

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            # print('request body: '+str(request.body))
            if request.body:
                json_data = json.loads(request.body.decode('UTF-8'))
                
                status = json_data.get('status', {})
                payment_date = json_data.get('payment_date', {})
                reference = json_data.get('reference', {})
                currency = json_data.get('currency', {})
                status_code = json_data.get('status_code', {})
                charge = json_data.get('charge', {})
                tokenized = json_data.get('tokenized', {})

                source = json_data.get('source', {})                
                source_object = source.get('object', {})
                source_type = source.get('type', {})
                source_number = source.get('number', {})

                processor_transaction_id = source.get('processor_transaction_id', {})
                source_reference = source.get('reference', {})                        
                amount = json_data.get('amount', {})
                processor_transaction_id = json_data.get('processor_transaction_id', {})
                transaction_uuid = json_data.get('transaction_uuid', {})
                amount_after_charge = json_data.get('amount_after_charge', {})
                message = json_data.get('message', {})
                error_fields = json_data.get('error_fields', {})

                metadata = json_data.get('metadata', {})                
                metadata_order_id = metadata.get('order_id', {})
                metadata_product_name = metadata.get('product_name', {})
                metadata_product_description = metadata.get('product_description', {})                

                callback = MyBusinessPayPaymentCallbacks(status=status, payment_date=payment_date, reference=reference, currency=currency, status_code=status_code, charge=charge, tokenized=tokenized, source=source, source_object=source_object, source_type=source_type, source_number=source_number, source_reference=source_reference, amount=amount, transaction_uuid=transaction_uuid, amount_after_charge=amount_after_charge, message=message, processor_transaction_id=processor_transaction_id, error_fields=error_fields, metadata=metadata, metadata_order_id=metadata_order_id, metadata_product_description=metadata_product_description)
                callback.save()

                if status == 'successful':   
                    response = updatevotes('mybusinesspay', metadata_order_id, transaction_uuid)  
                    
                    # if source_object == 'mobile_money': 
                    #     response = updatevotes_viaussd(metadata_order_id, metadata_order_id, transaction_uuid)  
                    # else:
                    #     response = updatevotes_viacard(metadata_order_id, transaction_uuid)  
                    if response == 'success':
                        return HttpResponse('Payment Callback Succeeded')
                    else:
                        return HttpResponse('Payment Callback Failed because '+str(response))
                else:
                    return HttpResponse('Payment Callback Failed')
            
            else:
                return HttpResponse('No Data Provided')
                
        except Exception as e:
            # print('mybizpay post callback error: '+str(e))
            return HttpResponse('Error at '+str(e))

        return HttpResponse('MyBusinessPay USSD Callback Reached')

class MyBusinessPayUSSDCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MyBusinessPayUSSDCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('MyBusinessPay USSD Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
            
            status = json_data['status']
            clienttransid = json_data['clienttransid']
            clientreference = json_data['clientreference']
            telcotransid = json_data['telcotransid']
            transactionid = json_data['transactionid']
            reason = json_data['reason']
            statusdate = json_data['statusdate']

            callback = MyBusinessPayUSSDCallbacks(status=status, clienttransid=clienttransid, clientreference=clientreference, telcotransid=telcotransid, transactionid=transactionid, reason=reason, statusdate=statusdate)
            callback.save()

            if status == 'PAID':                
                response = updatevotes('mybusinesspay', clientreference, transactionid)
                if response == 'success':
                    return HttpResponse('Payment USSD Callback Succeeded')
            elif status == 'FAILED':
                return HttpResponse('Payment Callback Failed')
            else:
                return HttpResponse('Payment Callback Error')
        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('MyBusinessPay USSD Callback Reached')

class MyBusinessPayCashoutCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MyBusinessPayCashoutCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('MyBusinessPay Cashout Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4  

            status = json_data['status']
            clienttransid = json_data['clienttransid']
            clientreference = json_data['clientreference']
            telcotransid = json_data['telcotransid']
            transactionid = json_data['transactionid']
            reason = json_data['reason']
            statusdate = json_data['statusdate']

            callback = MyBusinessPayCashoutCallbacks(status=status, clienttransid=clienttransid, clientreference=clientreference, telcotransid=telcotransid, transactionid=transactionid, reason=reason, statusdate=statusdate)
            callback.save()

            if status == 'PAID':                
                return HttpResponse('Cashout Callback Succeeded')
            elif status == 'FAILED':
                return HttpResponse('Cashout Callback Failed')
            else:
                return HttpResponse('Cashout Callback Error')
        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('MyBusinessPay Cashout Callback Reached')

class MyBusinessPayCardSuccessfulCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MyBusinessPayCardSuccessfulCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('MyBusinessPay Card Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4            
            
            status = json_data['status']
            reason = json_data['reason']
            transactionid = json_data['transactionid']
            clienttransid = json_data['clienttransid']
            referenceid = json_data['clientreference']
            statusdate = json_data['statusdate']

            callback = MyBusinessPayCardCallbacks(status=status, reason=reason, transactionid=transactionid, clienttransid=clienttransid, referenceid=referenceid, statusdate=statusdate)
            callback.save()

            if status == 'PAID':
                # response = updatevotes_viacard(clienttransid, transactionid)
                response = updatevotes('mybusinesspay', referenceid, transactionid)
                if response == 'success':
                    return HttpResponse('Payment Card Callback Succeeded')
            elif status == 'FAILED':
                return HttpResponse('Payment Card Callback Failed')
            else:
                return HttpResponse('Payment Card Callback Error')
            
        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('MyBusinessPay Card Callback Reached')

class MyBusinessPayCardFailureCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(MyBusinessPayCardFailureCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('MyBusinessPay Card Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
                
            status = json_data['status']
            reason = json_data['reason']
            transactionid = json_data['transactionid']
            clienttransid = json_data['clienttransid']
            referenceid = json_data['clientreference']
            statusdate = json_data['statusdate']

            callback = MyBusinessPayCardCallbacks(status=status, reason=reason, transactionid=transactionid, clienttransid=clienttransid, referenceid=referenceid, statusdate=statusdate)
            callback.save()

        except Exception as e:
            return HttpResponse('Error at '+str(e))

        return HttpResponse('MyBusinessPay Card Callback Reached')
########### MyBusinessPay Callbacks #############

########### Hubtel Callbacks #############
# Hubtel Callbacks
class HubtelCallbackView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(HubtelCallbackView, self).dispatch(request, *args, **kwargs)

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponse('Hubtel Callback Reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        try:
            json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4            
            print(f'Hubtel Callback Payload: {json_data}')
            Message = json_data['Status']
            ResponseCode = json_data['ResponseCode']
            Data = json_data['Data']
            transactionid = json_data['Data']['SalesInvoiceId']
            clientreference = json_data['Data']['ClientReference']
            
            
            callback = HubtelCallbacks(message=Message, responseCode=ResponseCode, data=Data)
            callback.save()
            
            if ResponseCode == '0000': 
                updatevotes('hubtel', clientreference, transactionid)
            else:
                return HttpResponse('Payment Callback Error')
        except Exception as e:
            print(f'Error at {e}')
            return HttpResponse('Error at '+str(e))

        return HttpResponse('Hubtel Callback Reached')

class HubtelReturnCallbackView(View):
    form_class = ''
    initial = {'': ''}
    template_hubtel_payment_successful = 'hubtel_payment_successful.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_hubtel_payment_successful, {  })

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

class HubtelCancelCallbackView(View):
    form_class = ''
    initial = {'': ''}
    template_hubtel_payment_failed = 'hubtel_payment_failed.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_hubtel_payment_failed, {  })

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        pass

########### Hubtel Callbacks #############


def updatevotes(provider, clienttransid, transactionid):
    try:
        # print(f'refid: {clienttransid}')
        request = None
        if provider == 'redde':
            request = PaymentRequests.objects.filter(clienttransid=clienttransid).last()
        elif provider == 'mybusinesspay':
            request = PaymentRequests.objects.filter(clientrefid=clienttransid).last()
        elif provider == 'hubtel':
            request = PaymentRequests.objects.filter(clienttransid=clienttransid).last()

        if request:
            # print(f'request found')
            request.paid = True
            request.datepaid = datetime.now().date()
            request.save()

            nomination = Nominations.objects.filter(nominee_code=request.custom_code).last()
            grossamount = float(request.amount)
            transactionamount = round(float(request.amount) * 0.022, 2)
            netamount = grossamount - transactionamount
            check_payment = Payments.objects.filter(request=request).last()
            if not check_payment:
                payment = Payments(request=request, nomination=nomination, transactionid=transactionid, grossamount=grossamount, transactionamount=transactionamount, netamount=netamount )
                payment.save()

                vote = Votes(payment=payment, nomination=nomination, votecount=request.value )
                vote.save()

                return 'success'
            else:
                return 'payment already exist'
        else:
            # print(f'Request not found')
            return 'no request found'

    except Exception as e:
        # print(f'update votes error : {e}')
        return HttpResponse('Error at '+str(e))

    return 'success'


def updatevotes_viaussd(clientrefid, clienttransid, transactionid):
    try:
        request = PaymentRequests.objects.filter(clientrefid=clientrefid).last()
        if clienttransid:
            request.clienttransid = clienttransid
        request.paid = True
        request.datepaid = datetime.now().date()
        request.save()

        nomination = Nominations.objects.filter(nominee_code=request.custom_code).last()
        grossamount = float(request.amount)
        transactionamount = round(float(request.amount) * 0.022, 2)
        netamount = grossamount - transactionamount
        check_payment = Payments.objects.filter(request=request).last()
        if not check_payment:
            payment = Payments(request=request, nomination=nomination, transactionid=transactionid, grossamount=grossamount, transactionamount=transactionamount, netamount=netamount )
            payment.save()

            vote = Votes(payment=payment, nomination=nomination, votecount=request.value )
            vote.save()

            return 'success'
        else:
            return 'payment already exist'
    except Exception as e:
        return HttpResponse('Error at '+str(e))

    return 'success'

def updatevotes_viacard(clienttransid, transactionid):
    try:
        request = PaymentRequests.objects.filter(clientrefid=clienttransid).last()
        # request.clienttransid = clienttransid
        request.paid = True
        request.datepaid = datetime.now().date()
        request.save()

        nomination = Nominations.objects.filter(nominee_code=request.custom_code).last()
        grossamount = float(request.amount)
        transactionamount = round(float(request.amount) * 0.022, 2)
        netamount = grossamount - transactionamount
        check_payment = Payments.objects.filter(request=request).last()
        if not check_payment:
            payment = Payments(request=request, nomination=nomination, transactionid=transactionid, grossamount=grossamount, transactionamount=transactionamount, netamount=netamount )
            payment.save()

            vote = Votes(payment=payment, nomination=nomination, votecount=request.value )
            vote.save()

            return 'success'
        else:
            return 'payment already exist'
    except Exception as e:
        return HttpResponse('Error at '+str(e))

    return 'success'

class AsoribaLandPaymentSuccessfulView(View):	
    template_dashboard = 'dashboard.html'
    template_farmpaidthankyou = 'farmpaidthankyou.html'
    template_farmpaymentfailed = 'farmpaymentfailed.html'

    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        amount = request.GET['amount']
        currency = request.GET['currency']
        message = request.GET['message']
        order_id = request.GET['metadata[order_id]']
        product_name = request.GET['metadata[product_name]']
        
        status = request.GET['status']
        statuscode = request.GET['status_code']
        transaction_uuid = request.GET['transaction_uuid']

        # return HttpResponse(status)

        if status == 'successful' and statuscode == '100':
            pass
        else:
            pass
        
        return HttpResponse('reached')

    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponse('reached')

