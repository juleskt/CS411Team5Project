from django.shortcuts import render, redirect
from SecretConfigs import *
import requests
import Search.forms as searchForms

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def index(request):
    # Initial landing page for the site

    # If the user has not logged in yet (cookie doesn't exist or we don't have a user session)
    if request.COOKIES.get('amazon_Login_state_cache', 'none') is 'none' or request.session.get('user') is None:
        return render(request, 'login.html')

    # If the user is already logged in (have session cookie)
    else:
        request.session['amazonLoginCache'] = request.COOKIES.get('amazon_Login_state_cache')

        # print(request.session['user'])

        # Redirect via name given in MealBoxV1.urls
        return redirect('search')


def handleLogin(request):
    # Page that handles login after the user signs in via Amazon

    # The Login with Amazon API will always https GET after logging in
    if request.method == 'GET':

        # Acquire the access token from the GET params to send back to Amazon
        accessToken = request.GET.get('access_token')

        # Send the access token back to Amazon for an access request
        accessRequest = requests.get('https://api.amazon.com/auth/o2/tokeninfo?access_token=' + accessToken)
        accessRequestJSON = accessRequest.json()

        if accessRequestJSON['aud'] != SecretConfigs.amazonClientID():
            # the access token does not belong to us
            raise BaseException("Invalid Token")

        # Store the access token in the session
        request.session['amazonAcessToken'] = accessRequestJSON

        # exchange the access token for user profile
        userProfileUrl = 'https://api.amazon.com/user/profile'
        userProfileHeader = {'Authorization': 'bearer ' + accessToken}
        userProfileRequest = requests.get(userProfileUrl, headers=userProfileHeader)
        userProfile = userProfileRequest.json()

        print("%s %s %s" % (userProfile['name'], userProfile['email'], userProfile['user_id']))

        request.session['user'] = userProfile
        request.session['amazonLoginCache'] = request.COOKIES.get('amazon_Login_state_cache')

        # Redirect via name given in MealBoxV1.urls
        return redirect('search')
