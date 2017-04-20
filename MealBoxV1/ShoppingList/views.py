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

    if request.session.get('shopping_list') is None:
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

        try:
            for i, product in enumerate(products):
                productData['result_number'] = i
                productData['product_title'] = product.title
                productData['product_asin'] = product.asin
                productData['product_medium_image'] = product.large_image_url
                productData['product_list_price'] = str(product.list_price)
                productData['product_brand'] = product.brand
                productData['product_formatted_price'] = product.formatted_price
                productData['detail_page_url'] = product.detail_page_url
                productData['product_offer_id'] = product.offer_id
                productData['product_reviews'] = product.reviews[1]

                jsonProducts.append(productData)
                productData = {}

            jsonWrapper = {}
            jsonWrapper['products'] = jsonProducts
            jsonWrapper['ingredient_name'] = ingredient

            print(jsonWrapper)

            return render(request, 'shoppingListModal.html', {'products': jsonWrapper['products'], 'ingredient_name': ingredient})

        except:
            return render(request, 'shoppingListModal.html', {'error': True})
    else:
      return Http404()


def addToAmazonCart(request):
    if request.method == 'POST':
        productASIN = request.POST.get('amazonOfferID')
        print(productASIN)

        return HttpResponse()

    else:
        return Http404()


def removeFromList(request):
    if request.method == 'POST':
        recipeIDToRemove = request.POST.get('recipeID')

        if request.session.get('shopping_list') is not None:
            print("Shopping list before remove:", request.session['shopping_list'])
            request.session['shopping_list'].remove(recipeIDToRemove)
            print("Shopping list after remove:", request.session['shopping_list'])

        return HttpResponse()

    else:
        return Http404()

def quickAddToCart(request):
    return HttpResponse()