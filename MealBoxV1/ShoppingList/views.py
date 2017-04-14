from django.shortcuts import render

# Create your views here.

from Search.searchAndAddSql import *

def index(request):
    recipeList = []

    recipeList.append(searchDBForRecipe(request.session['recipe_id']))
    return render(request, 'shoppingList.html', {'shopping_list': recipeList})
