from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from amazon.api import AmazonAPI
from SecretConfigs import *

# Create your views here.
from Search.searchAndAddSql import *

def index(request):
    ingredientsList = []

    if 'shopping_list' not in request.session:
        request.session['shopping_list'] = []
    else:
        request.session['shopping_list'] = list(set(request.session['shopping_list']))

    for recipeID in request.session['shopping_list']:
        ingredientsList.append(getIngredientsFromRecipeID(recipeID))

    print(ingredientsList)
    print("Shopping list:", request.session['shopping_list'])

    return render(request, 'shoppingList.html', {'ingredients_list' : ingredientsList})


def getAmazonResultsForModal(request):
    if request.method == 'POST':
        ingredient = request.POST.get('ingredientName')

        amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())
        products = amazon.search(Keywords=ingredient, SearchIndex='All')

        for i, product in enumerate(products):
           print (i, product.title, product.asin)

        return HttpResponse(json.dumps({'ingredient_name': ingredient}), content_type='application/json')
