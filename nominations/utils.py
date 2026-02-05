import re
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify

def generate_slug(cls, value):
    count = 1
    slug = slugify(value)
    if not isinstance(cls, type):
        cls = cls.__class__
 
    def _get_query(cls, **kwargs):
        if cls.objects.filter(**kwargs).count():
            return True
 
    while _get_query(cls, slug=slug):
        slug = slugify(u'{0}-{1}'.format(value, count))
        # make sure the slug is not too long
        while len(slug) > cls._meta.get_field('slug').max_length:
            value = value[:-1]
            slug = slugify(u'{0}-{1}'.format(value, count))
        count = count + 1
    return slug


def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated:
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view

def generate_token():
	return get_random_string(
        length=24, allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def generate_votecode():
	return get_random_string(
        length=4, allowed_chars = '0123456789')

def generate_username():
    return get_random_string(
        length=5, allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def generate_password():
    return get_random_string(
        length=5, allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields, search_type):
    '''
       Returns a query, that is a combination of Q objects. That combination
       aims to search keywords within a model by testing the given search fields. 
        search_type values:
            * 0 - match if string starts with any of the searched words separated by space
            * 1 - match if string contains any of the searched words separated by space
            * 2 - match if string is exactly any of the searched words separated by space
            * 3 - match if string contain whole search string (not split to keywords)
    '''
    
    query = None # Query to search for every search term

    # if match whole string contains
    if search_type == 3:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: query_string})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    else:
        terms = normalize_query(query_string)
        for term in terms:
            or_query = None # Query to search for a given term in each field
            for field_name in search_fields:
                # if start_with = true, search only terms that match the start of the string
                if search_type == 0:
                    q = Q(**{"%s__istartswith" %field_name: term})
                elif search_type == 1:
                    q = Q(**{"%s__icontains" % field_name: term})
                elif search_type == 2:
                    q = Q(**{"%s__iexact" % field_name: term})


                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query | or_query
    return query
