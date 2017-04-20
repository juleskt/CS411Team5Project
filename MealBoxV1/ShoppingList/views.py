from django.shortcuts import render
from django.http import HttpResponse, Http404
from django import template
import json
from amazon.api import AmazonAPI
from SecretConfigs import *
from django.template.loader_tags import BlockNode, ExtendsNode
from django.template import loader, Context, RequestContext
from django import template

register = template.Library()

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


@register.inclusion_tag('shoppingListModal.html')
#@render_to('shoppingListModal.html')
def getAmazonResultsForModal(request):
    if request.method == 'POST':
        ingredient = request.POST.get('ingredientName')

        amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())
        products = amazon.search(Keywords=ingredient, SearchIndex='All')#, ItemPage ='1')

        jsonProducts = []
        #jsonProducts['ingredient_name'] = ingredient
        productData = {}

        for i, product in enumerate(products):
            productData['result_number'] = i
            productData['product_title'] = product.title
            productData['product_asin'] = product.asin
            productData['product_medium_image'] = product.medium_image_url
            productData['product_list_price'] = str(product.list_price)
            productData['product_brand'] = product.brand
            productData['product_formatted_price'] = product.formatted_price
            productData['detail_page_url'] = product.detail_page_url
            productData['offer_url'] = product.offer_url

            jsonProducts.append(productData)
            productData = {}

        jsonWrapper = {}
        jsonWrapper['products'] = jsonProducts
        jsonWrapper['ingredient_name'] = ingredient

        print(jsonWrapper)

        return render(request, 'shoppingListModal.html', {'products': jsonWrapper['products'], 'ingredient_name': ingredient})
    else:
      return Http404()


def addToAmazonCart(request):
    if request.method == 'POST':
        productASIN = request.POST.get('amazonASIN')
        print(productASIN)

        return HttpResponse()

    else:
        return Http404()