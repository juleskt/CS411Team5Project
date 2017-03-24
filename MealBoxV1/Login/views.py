from django.shortcuts import render
from SecretConfigs import *
#from .forms import *
# Create your views here.


def index(request):
    return render(request, 'login.html')