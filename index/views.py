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

from .models import *
from nominations.models import *
from awards.models import *
from events.models import *
from blog.models import *

class MainView(View):
    template_main = 'index.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        blog = Blog.objects.filter(active=True).order_by('-id')[:8]
        return render(request, self.template_main, { 'blog':blog   })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('index', kwargs={  }, params={ }))

class HAGMoreInfoView(View):
    template_hag_more_info = 'hag_more_info.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_hag_more_info, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_hag_more_info, { })

class VoteNowView(View):
    template_votenow = 'votenow.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        category_get = request.GET.get('category')
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        category = None
        if awardscheme and category_get:
            category = NominationCategories.objects.filter(scheme=awardscheme, id=category_get).last()
        
        categories = NominationCategories.objects.filter(scheme=awardscheme)
        

        if category:
            allnominees = Nominations.objects.filter(category__scheme=awardscheme, category=category, approved=True).order_by('id')
        else:
            allnominees = Nominations.objects.filter(category__scheme=awardscheme, approved=True).order_by('id')
        paginator = Paginator(allnominees, 120) # Show 20 contacts per page        
        nominees = paginator.get_page(page)
        return render(request, self.template_votenow, { 'awardscheme':awardscheme, 'nominees':nominees, 'categories':categories, 'category':category,  })       
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('vote', kwargs={  }, params={     }))

class VoteView(View):
    template_vote = 'vote.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        code = request.GET.get('code')
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        nominee = Nominations.objects.filter(nominee_code=code, approved=True).last()
        voteonhold = False
        if nominee:
            return render(request, self.template_vote, { 'code':code, 'nominee':nominee, 'voteonhold':voteonhold })   
        else:
            return HttpResponseRedirect(build_url('votenow', kwargs={ }, params={ }))    
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('vote', kwargs={  }, params={     }))

class AboutView(View):
    template_about = 'about.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_about, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_about, { })

class TheBoardView(View):
    template_theboard = 'theboard.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        hagteamid = request.GET.get('id')
        hagteammember = HAGTeam.objects.filter(id=hagteamid, boardmember=True, active=True).last()
        hagteam = HAGTeam.objects.filter(boardmember=True, active=True).order_by('order_id')

        return render(request, self.template_theboard, { 'hagteammember':hagteammember, 'hagteam':hagteam })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_theboard, { })

class TheTeamView(View):
    template_theteam = 'theteam.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        hagteamid = request.GET.get('id')
        hagteammember = HAGTeam.objects.filter(id=hagteamid, teammember=True, active=True).last()
        hagteam = HAGTeam.objects.filter(teammember=True, active=True).order_by('order_id')

        return render(request, self.template_theteam, { 'hagteammember':hagteammember, 'hagteam':hagteam })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_theteam, { })

class SponsorshipsView(View):
    template_sponsorships = 'sponsorships.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_sponsorships, {  })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_sponsorships, { })


class EventsView(View):
    template_events = 'events.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        allevents = Events.objects.filter().order_by('-id')
        paginator = Paginator(allevents, 18) # Show 20 contacts per page        
        events = paginator.get_page(page)
        return render(request, self.template_events, { 'events':events })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_events, { })

class NominationsView(View):
    template_nominations = 'nominations.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return HttpResponseRedirect(reverse('nominate'))
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nominations, { })

class NominateView(View):
    template_nominate = 'nominate.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        nominationcategories = ''
        if awardscheme:
            allnominationcategories = NominationCategories.objects.filter(scheme=awardscheme, active=True).order_by('id')
            paginator = Paginator(allnominationcategories, 30) # Show 20 contacts per page        
            nominationcategories = paginator.get_page(page)
        return render(request, self.template_nominate, {'awardscheme':awardscheme, 'nominationcategories':nominationcategories })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nominate, { })

class NominationListView(View):
    template_nominations = 'nominations.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        awardscheme = AwardSchemes.objects.filter(active=True).order_by('-id').last()
        nominationcategories = ''
        if awardscheme:
            allnominationcategories = NominationCategories.objects.filter(scheme=awardscheme, active=True).order_by('id')
            paginator = Paginator(allnominationcategories, 30) # Show 20 contacts per page        
            nominationcategories = paginator.get_page(page)
        return render(request, self.template_nominations, {'awardscheme':awardscheme, 'nominationcategories':nominationcategories })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nominations, { })

class NominationTipsView(View):
    template_nomination_tips = 'nomination_tips.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_nomination_tips, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nomination_tips, { })

class NominationRulesView(View):
    template_nomination_rules = 'nomination_rules.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_nomination_rules, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nomination_rules, { })

class NominationGuidelinesView(View):
    template_nomination_guidelines = 'nomination_guidelines.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_nomination_guidelines, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nomination_guidelines, { })

class NominationEntryView(View):
    template_nomination_entry = 'nomination_entry.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_nomination_entry, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_nomination_entry, { })

class AwardsProcessView(View):
    template_awards_process = 'awards_process.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_awards_process, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_awards_process, { })

class AwardsView(View):
    template_awards = 'awards.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        awards = Awards.objects.filter()
        return render(request, self.template_awards, { 'awards':awards })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_awards, { })

class BlogView(View):
    template_blogs = 'blogs.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        blogs = Awards.objects.filter()
        return render(request, self.template_blogs, { 'blogs':blogs })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_blogs, { })

class GalleryView(View):
    template_gallery = 'gallery.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        allgalleries = Galleries.objects.filter().order_by('-id')
        paginator = Paginator(allgalleries, 16) # Show 20 contacts per page            
        galleries = paginator.get_page(page)
        # gallery = Awards.objects.filter()
        return render(request, self.template_gallery, { 'galleries':galleries })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_gallery, { })

class ContactsView(View):
    template_contacts = 'contacts.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_contacts, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_contacts, { })


class EmailSubscriptionView(View):
    """This is responsible for detecting get method and redirecting """

    def get(self, request):
        subsribed = False
        if EmailSubscription.objects.filter(email=request.GET.get('subscriberemail'), code=request.GET.get('code')):
            EmailSubscription.objects.filter(email=request.GET.get('subscriberemail')).update(subscriptionstatus=False)
            subscribed = True
        else:
            subscribed = False
        return HttpResponseRedirect(
            build_url('emailunsubscription_thankyou', kwargs={}, params={'subscribed': subscribed}))

    """This is responsible for detecting post method and processing information """

    def post(self, request):
        if not EmailSubscription.objects.filter(email=str(request.POST.get('subscriberemail') or '')):
            EmailSubscription.objects.create(email=str(request.POST.get('subscriberemail') or ''), subscriptionstatus=True)
        # elif EmailSubscription.objects.filter(email=str(request.POST.get('subscriberemail') or ''), subscriptionstatus=False):
        #     EmailSubscription.objects.filter(email=str(request.POST.get('subscriberemail') or '')).update(subscriptionstatus=True)
            
        # messages.success(request, 'You have subscribed successfully')

        # # send mail
        # recipients = str(request.POST.get('subscriberemail') or '')
        # subject = 'Newsletter Subscription Successful'
        # listobj = []
        # sender_message_data = {'subject': subject, 'fromAddr': '', 'fromName': '', 'toAddr': str(recipients or ''),
        #                        'replyTo': '', 'template': 'emailsubscription', 'rawMessage': '', 'userId': ''}
        # listobj.append(sender_message_data)

        # email_result = bulkemailsender(request, listobj)
        
        # if email_result == True:
        return HttpResponseRedirect(build_url('emailsubscription_thankyou', kwargs={}, params={}))

class EmailSubscriptionThankYouView(View):
    form_class = ''
    initial = {'': ''}
    template_emailsubscriptionthankyou = 'emailsubscriptionthankyou.html'

    """This is responsible for detecting get method and redirecting """

    def get(self, request):
        return render(request, self.template_emailsubscriptionthankyou, {})

    """This is responsible for detecting post method and processing information """

    def post(self, request):
        return render(request, self.template_emailsubscriptionthankyou, {})

class EmailUnSubscriptionThankYouView(View):
    form_class = ''
    initial = {'': ''}
    template_emailunsubscriptionthankyou = 'emailunsubscriptionthankyou.html'

    """This is responsible for detecting get method and redirecting """

    def get(self, request):
        subscribed = request.GET.get('subscribed')
        return render(request, self.template_emailunsubscriptionthankyou, {'subscribed': subscribed})

    """This is responsible for detecting post method and processing information """

    def post(self, request):
        return render(request, self.template_emailunsubscriptionthankyou, {})

