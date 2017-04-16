from django.shortcuts import render
import requests

# Create your views here.
from Search.searchAndAddSql import *

def index(request):
    recipeList = []
    if 'shopping_list' not in request.session:
        request.session['shopping_list'] = []
    for recipe in request.session['shopping_list']:
        recipeList.append(searchDBForRecipe(recipe))
    return render(request, 'shoppingList.html', {'recipes': recipeList})