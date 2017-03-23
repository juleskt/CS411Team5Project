# add to the top
from .forms import ContactForm, SearchForm, SearchResult
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json
from SecretConfigs import *

# add to your views
def contact(request):
    form_class = ContactForm
    return render(request, 'search.html', {'form': form_class,})


# Belongs to the search page
def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Grab the search string by keyword from POST as defined in forms.py
        searchString = str(request.POST.get('search', None))
        # redirect to a new URL:
        r = requests.get('http://food2fork.com/api/search?key=' + SecretConfigs.food2ForkKey() + '&q=' + searchString)
        # Serialize data for the searchResults.html template
        print(r.json())
        return render(request, 'searchResults.html', {'objects': r.json()['recipes'], 'searchString': searchString})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})
