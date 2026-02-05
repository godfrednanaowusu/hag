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
from .utils import *
from django.contrib import messages
from django.urls import *
from django.views import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import *
from django.core.paginator import *
from django.utils import translation
from vendor.functions.tasks import *
import uuid

from .models import *

class NominationView(View):
    template_nomination = 'nomination.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        if awardscheme.nominationopen:
            categoryid = request.GET.get('catid')
            category = NominationCategories.objects.filter(id=categoryid).last()
            if not category:
                category = NominationCategories.objects.filter().first()
            return render(request, self.template_nomination, {'awardscheme':awardscheme, 'category':category })
        else:
            messages.error(request, 'Nomination is not Open')
            return HttpResponseRedirect(build_url('nominations'))
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nomination, { })

class NominationReferenceView(View):
    form_class = NominationsForm
    initial = {'': ''}
    template_nomination_reference = 'nominations.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        page = request.GET.get('page')
        allnominationcategories = NominationCategories.objects.filter(scheme__id=awardscheme.id).order_by('id')
        paginator = Paginator(allnominationcategories, 18) # Show 20 contacts per page        
        nominationcategories = paginator.get_page(page)
        return render(request, self.template_nomination_reference, { 'awardscheme':awardscheme, 'nominationcategories':nominationcategories })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        refno = request.POST['referencenumber']
        nominationcheck = Nominations.objects.filter(category__scheme__id=awardscheme.id, referencenumber=refno).last()
        if nominationcheck:
            return HttpResponseRedirect(build_url('nomination_form', kwargs={  }, params={'referencenumber':refno, 'category':nominationcheck.category.name })) 
        else:
            messages.error(request, 'Nomination does not Exist')
            return HttpResponseRedirect(build_url('nominations', kwargs={  }, params={ })) 

       
        return render(request, self.template_nomination_reference, { 'form':form })

class NominationFormView(View):
    form_class = NominationsForm
    covid_form_class = Covid19NominationsForm
    initial = {'': ''}
    template_nomination_form = 'nomination_form.html'
    template_nomination_form_covid = 'nomination_form_covid.html'
    template_nomination_thanks = 'nomination_thanks.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        referencenumber = request.GET.get('referencenumber')
        category_get = request.GET.get('category')
        categories = NominationCategories.objects.filter(scheme=awardscheme, active=True)
        category = NominationCategories.objects.filter(id=category_get).last()
        nomination = Nominations.objects.filter(category__scheme__id=awardscheme.id, category__id=category.id, referencenumber=referencenumber).last()
        # return HttpResponse(nomination)
        if nomination:
            if category.name.lower() == 'covid-19 heroes':
                form = self.covid_form_class(instance=nomination)
            else:
                form = self.form_class(instance=nomination)
        else:
            if category.name.lower() == 'covid-19 heroes':
                form = self.covid_form_class()
            else:
                form = self.form_class()
        if category.name.lower() == 'covid-19 heroes':
            return render(request, self.template_nomination_form_covid, {'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })
        else:
            return render(request, self.template_nomination_form, {'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        categories = NominationCategories.objects.filter(scheme__id=awardscheme.id)
        category_get = request.POST['category']
        category = NominationCategories.objects.filter(id=category_get).last()
        nomination = ''
        if 'updateapplication' in request.POST:
            nomination = Nominations.objects.filter(category__scheme__id=awardscheme.id, id=request.POST['nominationid']).last()
            if category.name.lower() == 'covid-19 heroes':
                form = self.covid_form_class(request.POST, request.FILES, instance=nomination)
            else:
                form = self.form_class(request.POST, request.FILES, instance=nomination)        
            
            if form.is_valid():
                instance = form.save(commit=False)            
                # categ = NominationCategories.objects.filter(scheme__id=awardscheme.id, id=category.id).last()
                if category:
                    instance.category = category

                    if request.POST['clearphoto'] == 'clearphoto':
                        instance.nominee_photograph = None

                    if category.name.lower() == 'covid-19 heroes':
                        instance.votable = False

                    instance.save()
                    messages.success(request, 'Nomination Updated Successfully')
                    return HttpResponseRedirect(build_url('nomination_form_thanks', kwargs={ }, params={ })) 
                    # return render(request, self.template_nomination_thanks, { 'category':category, 'categories':categories, 'form':form })
                else:
                    messages.error(request, 'Category Not Available')
                    return render(request, self.template_nomination_form, {'category':category, 'categories':categories, 'form':form })
            else:
                messages.error(request, 'Nomination Update Failed')
                messages.error(request, form.errors)
                return render(request, self.template_nomination_form, { 'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })

        elif 'submitapplication' in request.POST:
            if category.name.lower() == 'covid-19 heroes':
                form = self.covid_form_class(request.POST, request.FILES)
            else:
                form = self.form_class(request.POST, request.FILES)        

            # form = self.form_class(request.POST, request.FILES)  
            # refno = str(uuid.uuid4())
            
            if form.is_valid():
                instance = form.save(commit=False)            
                # categ = NominationCategories.objects.filter(scheme__name=awardscheme.name, id=category).last()
                if category:
                    refno = str(uuid.uuid4())            
                    checkref = Nominations.objects.filter(referencenumber=refno).last()
                    if not checkref:
                        instance.referencenumber = refno
                    else:
                        refno = str(uuid.uuid4())
                        instance.referencenumber = refno
                        
                    votecode = generate_votecode()
                    checkcode = Nominations.objects.filter(nominee_code=votecode).last()
                    if not checkcode:
                        instance.nominee_code = votecode
                    else:
                        votecode = generate_votecode()
                        checkcode = Nominations.objects.filter(nominee_code=votecode).last()
                        if not checkcode:
                            instance.nominee_code = votecode

                    instance.category = category
                    # instance.referencenumber = refno
                    if category.name.lower() == 'covid-19 heroes':
                        instance.votable = False
                        
                    instance.save()
                    messages.success(request, 'Nomination Submitted Successfully')
                    messages.success(request, 'We will review the Nomination Form and get back to you')

                    try:
                        if category.name.lower() == 'covid-19 heroes':
                            ######### Send mail to Nominee ####################
                            subject = 'Nominated as a COVID-19 Hero'
                            message = 'Congratulations! <br><br> You have been nominated as a COVID-19 Hero at Humanitarian Award Global. We will review your Nomination and get back to you soon, in the meantime, if you have any queries, please send an email to info@humanitarianawardsglobal.com <br> This is your Reference Number: <b>'+refno+'</b> <br><br>Regards <br><b>Team, Humanitarian Awards Global. </b><br><small>Follow us on Facebook, Twitter, and Instagram to get all the update regarding the Humanitarian Awards Global.</small>'
                            html_message = placemessageontemplate('', message)
                            send_mail(subject, message, settings.EMAIL_ADMIN, [request.POST['nominee_emailaddress']], html_message=html_message)
                            ######################################################

                        else:
                            ######### Send mail to Nominee ####################
                            subject = 'Nominated for Humanitarian Awards'
                            message = 'Congratulations Change Maker! <br><br> You have been nominated for a Humanitarian Award Global. We will review your Nomination and get back to you soon, in the meantime, if you have any queries, please send an email to info@humanitarianawardsglobal.com <br> This is your Reference Number: <b>'+refno+'</b> <br><br>Regards <br><b>Team, Humanitarian Awards Global. </b><br><small>Follow us on Facebook, Twitter, and Instagram to get all the update regarding the Humanitarian Awards Global.</small>'
                            html_message = placemessageontemplate('', message)
                            send_mail(subject, message, settings.EMAIL_ADMIN, [request.POST['nominee_emailaddress']], html_message=html_message)
                            ######################################################

                        
                            ######### Send mail to Nominator ####################
                            subject = 'Nomination Submitted Successfully'
                            message = 'Thank you for Nominating for Humanitarian Awards Global. <br> Your Reference Number is <b>'+refno+'</b> <br> <br><br> <b>Management of Humanitarian Awards Global.</b> <br><small>Follow us on Facebook, Twitter, and Instagram to get all the update regarding the Humanitarian Awards Global.</small>'
                            html_message = placemessageontemplate('', message)
                            send_mail(subject, message, settings.EMAIL_ADMIN, [request.POST['nominator_emailaddress']], html_message=html_message)
                            ######################################################
                    except:
                        print('Email sending error')
                        
                    return HttpResponseRedirect(build_url('nomination_form_thanks', kwargs={  }, params={ })) 
                else:
                    messages.error(request, 'Category Not Available')
                    if category.name.lower() == 'covid-19 heroes':
                        return render(request, self.template_nomination_form_covid, { 'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })
                    else:
                        return render(request, self.template_nomination_form, { 'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })
            else:
                messages.error(request, 'Nomination Submission Failed')
                messages.error(request, form.errors)
                if category.name.lower() == 'covid-19 heroes':
                    return render(request, self.template_nomination_form_covid, { 'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })
                else:
                    return render(request, self.template_nomination_form, { 'awardscheme':awardscheme, 'nomination':nomination, 'category':category, 'categories':categories, 'form':form })

        if category.name.lower() == 'covid-19 heroes':
            return render(request, self.template_nomination_form_covid, { 'form':form })
        else:
            return render(request, self.template_nomination_form, { 'form':form })

class CreateRefidView(View):
    template_nomination = 'nomination.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        empty_nominations = Nominations.objects.filter(referencenumber='')
        for nom in empty_nominations:
            refno = str(uuid.uuid4())            
            checkref = Nominations.objects.filter(referencenumber=refno).last()
            if not checkref:
                nom.referencenumber = refno
                nom.save()
        
        return HttpResponseRedirect(build_url('nominations', kwargs={  }, params={ })) 
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('nominations', kwargs={  }, params={ })) 

class CreateVoteCodeView(View):
    template_nomination = 'nomination.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        allnominations = Nominations.objects.filter(category__scheme=awardscheme)
        for nom in allnominations:
            checkcode = ''
            votecode = generate_votecode()
            checkcode = Nominations.objects.filter(nominee_code=votecode).last()
            if not checkcode:
                nom.nominee_code = votecode
                nom.save()
            else:
                votecode = generate_votecode()
                checkcode = Nominations.objects.filter(nominee_code=votecode).last()
                if not checkcode:
                    nom.nominee_code = votecode
                    nom.save()
        
        return HttpResponseRedirect(build_url('nominations', kwargs={  }, params={ })) 
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('nominations', kwargs={  }, params={ })) 

# class TestEmailView(View):
#     template_nomination = 'nomination.html'
        
#     """This is responsible for detecting get method and redirecting """		
#     def get(self, request):
#         response = ''
#         try:
#             subject = 'Nomination Test Email'
#             message = 'Test email content'
#             # html_message = placemessageontemplate('', message)
#             response = send_mail(subject, message, settings.EMAIL_ADMIN, ['iamgodfredowusu@gmail.com'], html_message=message)
#             print(f'email response: {response}')
#         except Exception as e:
#             print(f'email error: {e}')
    
#         return HttpResponse(f'email tested: {response}')
    
#     """This is responsible for detecting post method and processing information """
#     def post(self, request):
#         return HttpResponseRedirect(build_url('test_email', kwargs={  }, params={ })) 


