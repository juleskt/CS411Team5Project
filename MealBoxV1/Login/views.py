from django.shortcuts import render
from SecretConfigs import *
import pycurl
import urllib
import urllib.parse
import json
import certifi
import requests

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def index(request):
    if request.COOKIES.get('amazon_Login_state_cache', 'none') is 'none' or request.session.get('user') is None:
        if request.method == 'GET':
            return render(request, 'login.html')
    else:
        amazonLoginCache = request.COOKIES.get('amazon_Login_state_cache')
        print(request.session['user'])

        return render(request, 'search.html', {'name': request.session['user']['name']})


def handleLogin(request):
    if request.method == 'GET':
        accessToken = request.GET.get('access_token')

        accessRequest = requests.get('https://api.amazon.com/auth/o2/tokeninfo?access_token=' + accessToken)
        accessRequestJSON = accessRequest.json()

        if accessRequestJSON['aud'] != SecretConfigs.amazonClientID():
            # the access token does not belong to us
            raise BaseException("Invalid Token")

        # exchange the access token for user profile
        userProfileUrl = 'https://api.amazon.com/user/profile'
        userProfileHeader = {'Authorization': 'bearer ' + accessToken}
        userProfileRequest = requests.get(userProfileUrl, headers=userProfileHeader)
        userProfile = userProfileRequest.json()

        print ("%s %s %s" % (userProfile['name'], userProfile['email'], userProfile['user_id']))

        request.session['user'] = userProfile

        return render(request, 'search.html', {'name': userProfile['name']})

        #renderSearchPage(request, userProfile['name'])


def renderSearchPage(request, username):
    return render(request, 'search.html', {'name': username})
