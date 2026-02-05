from social_django.models import UserSocialAuth
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse,  HttpResponseRedirect, JsonResponse


def get_user_avatar(request, backend, user, response, is_new=False, *args, **kwargs):
# def get_user_avatar(request, backend, details, response, social_user, storage, uid, user, *args, **kwargs):
    s = SessionStore()
    
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    elif backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    
    elif backend.name == 'google-oauth2':
        url = response['picture']

    # return HttpResponse(url)
    request.session['avatar_url'] = url
    return