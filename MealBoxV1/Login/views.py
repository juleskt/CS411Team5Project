from django.shortcuts import render
from SecretConfigs import *
import pycurl
import urllib
import urllib.parse
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def index(request):

    #q = request.GET['q']

    print (request)

    if request.method == 'GET':
 #       if request.COOKIES is not None:
  #          return render(request, 'login.html')

#    else:
    ##if q is not None and q != '':
        b = StringIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://api.amazon.com/auth/o2/tokeninfo?access_token=" + urllib.parse.quote_plus(SecretConfigs.amazonClientSecret()))
        c.setopt(pycurl.SSL_VERIFYPEER, 1)
        c.setopt(pycurl.WRITEFUNCTION, b.write)

        c.perform()
        d = json.loads(b.getvalue())

        if d['aud'] != SecretConfigs.amazonClientID():
            # the access token does not belong to us
            raise BaseException("Invalid Token")

        # exchange the access token for user profile
        b = StringIO()

        c = pycurl.Curl()
        c.setopt(pycurl.URL, "https://api.amazon.com/user/profile")
        c.setopt(pycurl.HTTPHEADER, ["Authorization: bearer " + SecretConfigs.amazonClientSecret()])
        c.setopt(pycurl.SSL_VERIFYPEER, 1)
        c.setopt(pycurl.WRITEFUNCTION, b.write)

        c.perform()
        d = json.loads(b.getvalue())

        print ("%s %s %s" % (d['name'], d['email'], d['user_id']))