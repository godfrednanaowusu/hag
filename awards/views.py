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

class AwardView(View):
    template_award = 'award.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        return render(request, self.template_award, { })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return render(request, self.template_award, { })
