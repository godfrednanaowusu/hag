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

class BlogView(View):
    template_blog = 'blog.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request):
        page = request.GET.get('page')
        allblog = Blog.objects.filter(active=True).order_by('-id')
        paginator = Paginator(allblog, 20)  # Show 20 blog per page
        blog = paginator.get_page(page)
        return render(request, self.template_blog, { 'blog':blog })
    
    """This is responsible for detecting post method and processing information """
    def post(self, request):
        return HttpResponseRedirect(build_url('blog', kwargs={  }, params={ }))

class BlogDetailView(View):
    template_blog_detail = 'blog_detail.html'
        
    """This is responsible for detecting get method and redirecting """		
    def get(self, request, identifier):
        blog = None
        related_blog = None
        stream_url = ''
        try:
            blog = Blog.objects.get(identifier=identifier, active=True)
            related_blog = Blog.objects.filter().exclude(identifier=blog.identifier).order_by('-id')[:10]
            
            # streamlink = str(blog.link or '')
            
            # if streamlink.startswith(('youtu', 'www')):
            #     streamlink = 'http://' + streamlink                
            
            # query = urlparse(streamlink)

            # if 'youtube' in query.hostname:
            #     if query.path == '/watch':
            #         stream_url = 'https://www.youtube.com/embed/'+ parse_qs(query.query)['v'][0]+'?rel=0&showinfo=0&modestbranding=1'
            #     elif query.path.startswith(('/embed/', '/v/')):
            #         stream_url = 'https://www.youtube.com/embed/'+ query.path.split('/')[2]+'?rel=0&showinfo=0&modestbranding=1'
            # elif 'youtu.be' in query.hostname:
            #     stream_url = 'https://www.youtube.com/embed/'+ query.path[1:]+'?rel=0&showinfo=0&modestbranding=1'
            # else:
            #     messages.warning(request, 'There was a problem caused by '+str(query) )


        except Blog.DoesNotExist:
            return HttpResponseRedirect('index')   
                 
        return render(request, self.template_blog_detail, { 'blog':blog, 'stream_url':stream_url, 'related_blog':related_blog })
    
    
    """This is responsible for detecting post method and processing information """
    def post(self, request, identifier):
        return HttpResponseRedirect(build_url('blog', kwargs={  }, params={ }))

