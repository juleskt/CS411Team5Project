from django.shortcuts import render
from django.http import HttpResponse
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
           # print (i, product.title, product.asin)

            productData['result_number'] = i
            productData['product_title'] = product.title
            productData['product_asin'] = product.asin
            productData['product_medium_image'] = product.medium_image_url
            productData['product_list_price'] = str(product.list_price)

            jsonProducts.append(productData)
            productData = {}

        jsonWrapper = {}
        jsonWrapper['products'] = jsonProducts
        jsonWrapper['ingredient_name'] = ingredient

        print(jsonWrapper)

        #return HttpResponse(json.dumps({'ingredient_name': ingredient}), content_type='application/json')
        #return HttpResponse(json.dumps(jsonWrapper), content_type='application/json')
        #return render(request, 'shoppingListModal.html', {'products': jsonWrapper['products']})

        #dataContext = Context({'products': jsonWrapper['products']})

       # returnString = render_block_to_string('shoppingListModal.html', 'modal-body', dataContext)
       # return HttpResponse(returnString)

       # return request, {'products' : jsonWrapper['products']}

        return render(request, 'shoppingListModal.html', {'products': jsonWrapper['products'], 'ingredient_name': ingredient})

# https://www.djangosnippets.org/snippets/942/
def get_template(template):
  if isinstance(template, (tuple, list)):
    return loader.select_template(template)
  return loader.get_template(template)

# https://www.djangosnippets.org/snippets/942/
class BlockNotFound(Exception):
  pass

# https://www.djangosnippets.org/snippets/942/
def render_template_block(template, block, context):
  """
  Renders a single block from a template. This template should have previously been rendered.
  """
  return render_template_block_nodelist(template.nodelist, block, context)

# https://www.djangosnippets.org/snippets/942/
def render_template_block_nodelist(nodelist, block, context):
  for node in nodelist:
    if isinstance(node, BlockNode) and node.name == block:
      return node.render(context)
    for key in ('nodelist', 'nodelist_true', 'nodelist_false'):
      if hasattr(node, key):
        try:
          return render_template_block_nodelist(getattr(node, key), block, context)
        except:
          pass
  for node in nodelist:
    if isinstance(node, ExtendsNode):
      try:
        return render_template_block(node.get_parent(context), block, context)
      except BlockNotFound:
        pass
  raise BlockNotFound

# https://www.djangosnippets.org/snippets/942/
def render_block_to_string(template_name, block, dictionary=None, context_instance=None):
  """
  Loads the given template_name and renders the given block with the given dictionary as
  context. Returns a string.
  """
  dictionary = dictionary or {}
  t = get_template(template_name)
  if context_instance:
    context_instance.update(dictionary)
  else:
    context_instance = Context(dictionary)
  t.render(context_instance)
  return render_template_block(t, block, context_instance)

# https://www.djangosnippets.org/snippets/942/
def direct_block_to_template(request, template, block, extra_context=None, mimetype=None, **kwargs):
  """
  Render a given block in a given template with any extra URL parameters in the context as
  ``{{ params }}``.
  """
  if extra_context is None:
    extra_context = {}
  dictionary = {'params': kwargs}
  for key, value in extra_context.items():
    if callable(value):
      dictionary[key] = value()
    else:
      dictionary[key] = value
  c = RequestContext(request, dictionary)
  t = get_template(template)
  t.render(c)
  return HttpResponse(render_template_block(t, block, c), mimetype=mimetype)