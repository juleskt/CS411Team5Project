# add to the top
import json
import requests
from SecretConfigs import *
from bs4 import BeautifulSoup
from datetime import date, datetime
from django.db import connection, connections
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from .searchAndAddSql import *
from .forms import ContactForm, SearchForm, SearchResult


# add to your views
def contact(request):
    form_class = ContactForm
    return render(request, 'search.html', {'form': form_class})


# Belongs to the search page
def search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Grab the search string by keyword from POST as defined in forms.py
        searchString = str(request.POST.get('search', None))

        # UnComment below and comment out everything else for test queries
        #return render(request, 'searchResults.html', {'recipes': dummyQuery['recipes'], 'searchString': searchString})

        #Check the DB for the cached result
        cacheResult = searchDBCacheForSearch(searchString)

        if cacheResult is None:

            print("NOT IN CACHE")

            # Hit the API:
            r = requests.get('http://food2fork.com/api/search?key=' + SecretConfigs.food2ForkKey() + '&q=' + searchString)

            if r.json()['count'] > 5:
                insertSearchIntoDBCache(searchString, r.json())

            # Serialize data for the searchResults.html template
            return render(request, 'searchResults.html', {'recipes': r.json()['recipes'], 'searchString': searchString})

        else:
            # We want the second element of tuple because it is the third row in the cache db
            
            cachedDate = cacheResult[4]
            currentDate = datetime.today().date()

            dateDelta = currentDate - cachedDate

            print("Cached Date: ", cachedDate, "Current Date: ", currentDate, "Delta:", dateDelta.days)

            if dateDelta.days < 7:
                cacheResultDataColumn = json.loads(cacheResult[2])
                return render(request, 'searchResults.html', {'recipes': cacheResultDataColumn['recipes'], 'searchString': searchString})

            else:
                # Hit the API:
                r = requests.get('http://food2fork.com/api/search?key=' + SecretConfigs.food2ForkKey() + '&q=' + searchString)

                if r.json() is None:
                    r = requests.get('http://food2fork.com/api/search?key=' + SecretConfigs.food2ForkBackupKey() + '&q=' + searchString)

                if r.json()['count'] > 5:
                    updateSearchIntoDBCache(searchString, r.json())
            
                return render(request, 'searchResults.html', {'recipes': r.json()['recipes'], 'searchString': searchString})
    # if a GET (or any other method) we'll create a blank form
    else:
        # If the user has not logged in yet (cookie doesn't exist or we don't have a user session)
        if request.COOKIES.get('amazon_Login_state_cache', 'none') is 'none' or request.session.get('user') is None:
            return redirect('index')

        form = SearchForm()

    return render(request, 'search.html', {'form': form, 'name': request.session['user']['user_name']})


# recipeID, recipeTitle, recipeDirections, recipeIngredientsUrl coming in from POST
def addRecipe(request):
    if request.method == 'POST':
        recipeIngredientsUrl = request.POST.get('recipeIngredientsUrl')

        recipeTitle = request.POST.get('recipeTitle')
        recipeID = request.POST.get('recipeID')
        recipeDirections = request.POST.get('recipeDirections')
        recipeImgURL = request.POST.get('recipeImageUrl')

        # If the recipe isn't in the DB, add it
        if not searchDBForRecipe(recipeID):
            addRecipeToDB(recipeID, recipeTitle, recipeDirections, recipeImgURL)

        # If the recipe isn't correlated to the user, make it so
        if not searchDBForSavedRecipe(recipeID, request.session['user']['user_amazon_id']):
            addSavedRecipeForUser(recipeID, request.session['user']['user_amazon_id'])

        # Get a dictionary for ingredients and directions from the URL
        ingredientsDict = getIngredientsFromF2FURL(recipeIngredientsUrl)
        ingredients = ingredientsDict['ingredients']
        rawIngredientsAndDescription = ingredientsDict['rawIngredients']

        # Loop through two lists at the same time
        for ingredient, rawDescription in zip(ingredients, rawIngredientsAndDescription):
            savedIngredient = searchDBForSavedIngredient(ingredient)

            if not savedIngredient:
                addIngredientToDB(ingredient)
                savedIngredient = searchDBForSavedIngredient(ingredient)

            addIngredientToRecipe(recipeID, savedIngredient[0]['ingredient_id'], rawDescription)


        return HttpResponse()

def deleteRecipe(request):
    if request.method == 'POST':
        recipeID = request.POST.get('recipeID')
        deleteSavedRecipeFromDB(recipeID, request.session['user']['user_amazon_id'])
        return HttpResponse()


def getIngredientsFromF2FURL(ingreidentsURL):
    ingreidentsHTML = requests.get(ingreidentsURL).text
    # Pass the source html to BeautifulSoup
    htmlParser = BeautifulSoup(ingreidentsHTML, 'lxml')
    # Look through li tags, and find itemprop attributes named ingredients
    htmlIngredients = htmlParser.findAll('li', {'itemprop': 'ingredients'})

    # Raw, unparsed ingredients with full description, will go into Recipe_ingredients_tbl as description
    rawIngredients = []
    # Ingredients in nested list form with some extraneous details
    parsedIngredientsList = []
    # Final list of ingredients, with only the ingredient
    parsedIngredients = []

    # Loop through the html tags and grab the ingredients + description (in the text member variable)
    for ingredient in htmlIngredients:
        rawIngredients.append(ingredient.text)

        # Remove non letters from the string, but keep spaces
        #parsedIngredients.append(''.join([i for i in ingredient.text if i.isalpha() or i is ' ']))

    for ingredient in rawIngredients:
        # Split the ingredient string by spaces
        ingredientSplit = ingredient.split()

        # Prepare a list for each ingredient
        ingredientList = []

        # If we removed a chunk in the last iteration, remove the next one too
        elementRemoved = False

        # Only add to the list if the chunk doesn't have numbers or parenthesis
        # Some recipes will have the amounts with the ingredient, we don't need this for Amazon search
        for chunk in ingredientSplit:
            # Can probs change to regex to make it more clean
            if not any(char.isdigit() or char is '(' or char is ')' for char in chunk):
                ingredientList.append(chunk)
            else:
                elementRemoved = True

        # If we removed something, remove the first item left. Heuristically, '1 tsp sugar' would look like
        # 'tsp sugar' after the above extraction, we want to remove tsp. Values are usually followed by units.
        if elementRemoved:
            ingredientList.pop(0)
        parsedIngredientsList.append(ingredientList)

    # Combine the lists into space-separated words and remove everything after the first comma character, if it exists
    # Also truncate anything after OR statements if they exist and remove newline characters
    # Add to final list
    for parsedIngredient in parsedIngredientsList:
        ingredientToAdd = ' '.join(parsedIngredient).split(',')[0]
        ingredientToAdd = ingredientToAdd.split('OR')[0]
        ingredientToAdd = ingredientToAdd.split('or')[0]
        parsedIngredients.append(ingredientToAdd)

    return {'ingredients': parsedIngredients, 'rawIngredients': rawIngredients}


def addToShoppingList(request):
    if request.method == 'POST':
        if 'shopping_list' not in request.session:
            request.session['shopping_list'] = []

        request.session['shopping_list'] = request.session['shopping_list'] + [request.POST.get('recipeID')]

    return HttpResponse()
