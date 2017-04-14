# add to the top
from .forms import ContactForm, SearchForm, SearchResult
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
import requests
import json
from SecretConfigs import *
from datetime import date, datetime
from django.db import connection, connections
from .searchAndAddSql import *
from bs4 import BeautifulSoup

# add to your views
def contact(request):
    form_class = ContactForm
    return render(request, 'search.html', {'form': form_class})

dummyQuery = {"count": 30, "recipes": [{"publisher": "101 Cookbooks", "f2f_url": "http://food2fork.com/view/47746", "title": "Best Pizza Dough Ever", "source_url": "http://www.101cookbooks.com/archives/001199.html", "recipe_id": "47746", "image_url": "http://static.food2fork.com/best_pizza_dough_recipe1b20.jpg", "social_rank": 100.0, "publisher_url": "http://www.101cookbooks.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/46956", "title": "Deep Dish Fruit Pizza", "source_url": "http://thepioneerwoman.com/cooking/2012/01/fruit-pizza/", "recipe_id": "46956", "image_url": "http://static.food2fork.com/fruitpizza9a19.jpg", "social_rank": 100.0, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35477", "title": "Pizza Dip", "source_url": "http://www.closetcooking.com/2011/03/pizza-dip.html", "recipe_id": "35477", "image_url": "http://static.food2fork.com/Pizza2BDip2B12B500c4c0a26c.jpg", "social_rank": 99.99999999999994, "publisher_url": "http://closetcooking.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/41470", "title": "Cauliflower Pizza Crust (with BBQ Chicken Pizza)", "source_url": "http://www.closetcooking.com/2013/02/cauliflower-pizza-crust-with-bbq.html", "recipe_id": "41470", "image_url": "http://static.food2fork.com/BBQChickenPizzawithCauliflowerCrust5004699695624ce.jpg", "social_rank": 99.9999999999994, "publisher_url": "http://closetcooking.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35478", "title": "Pizza Quesadillas (aka Pizzadillas)", "source_url": "http://www.closetcooking.com/2012/11/pizza-quesadillas-aka-pizzadillas.html", "recipe_id": "35478", "image_url": "http://static.food2fork.com/Pizza2BQuesadillas2B2528aka2BPizzadillas25292B5002B834037bf306b.jpg", "social_rank": 99.99999999999835, "publisher_url": "http://closetcooking.com"}, {"publisher": "Two Peas and Their Pod", "f2f_url": "http://food2fork.com/view/54454", "title": "Sweet Potato Kale Pizza with Rosemary & Red Onion", "source_url": "http://www.twopeasandtheirpod.com/sweet-potato-kale-pizza-with-rosemary-red-onion/", "recipe_id": "54454", "image_url": "http://static.food2fork.com/sweetpotatokalepizza2c6db.jpg", "social_rank": 99.9999999991673, "publisher_url": "http://www.twopeasandtheirpod.com"}, {"publisher": "My Baking Addiction", "f2f_url": "http://food2fork.com/view/2ec050", "title": "Pizza Dip", "source_url": "http://www.mybakingaddiction.com/pizza-dip/", "recipe_id": "2ec050", "image_url": "http://static.food2fork.com/PizzaDip21of14f05.jpg", "social_rank": 99.99999999826605, "publisher_url": "http://www.mybakingaddiction.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/6fab1c", "title": "Pizza Potato Skins", "source_url": "http://thepioneerwoman.com/cooking/2013/04/pizza-potato-skins/", "recipe_id": "6fab1c", "image_url": "http://static.food2fork.com/pizza3464.jpg", "social_rank": 99.99999999760887, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "Bon Appetit", "f2f_url": "http://food2fork.com/view/49346", "title": "No-Knead Pizza Dough", "source_url": "http://www.bonappetit.com/recipes/2012/03/no-knead-pizza-dough", "recipe_id": "49346", "image_url": "http://static.food2fork.com/nokneadpizzadoughlahey6461467.jpg", "social_rank": 99.99999999743466, "publisher_url": "http://www.bonappetit.com"}, {"publisher": "Simply Recipes", "f2f_url": "http://food2fork.com/view/36453", "title": "Homemade Pizza", "source_url": "http://www.simplyrecipes.com/recipes/homemade_pizza/", "recipe_id": "36453", "image_url": "http://static.food2fork.com/pizza292x2007a259a79.jpg", "social_rank": 99.99999998833789, "publisher_url": "http://simplyrecipes.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35626", "title": "Taco Quesadilla Pizzas", "source_url": "http://www.closetcooking.com/2012/08/taco-quesadilla-pizza.html", "recipe_id": "35626", "image_url": "http://static.food2fork.com/Taco2BQuesadilla2BPizza2B5002B4417a4755e35.jpg", "social_rank": 99.99999998319973, "publisher_url": "http://closetcooking.com"}, {"publisher": "All Recipes", "f2f_url": "http://food2fork.com/view/17796", "title": "Jay\u2019s Signature Pizza Crust", "source_url": "http://allrecipes.com/Recipe/Jays-Signature-Pizza-Crust/Detail.aspx", "recipe_id": "17796", "image_url": "http://static.food2fork.com/237891b5e4.jpg", "social_rank": 99.99999997246182, "publisher_url": "http://allrecipes.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35097", "title": "Avocado Breakfast Pizza with Fried Egg", "source_url": "http://www.closetcooking.com/2012/07/avocado-breakfast-pizza-with-fried-egg.html", "recipe_id": "35097", "image_url": "http://static.food2fork.com/Avocado2Band2BFried2BEgg2BBreakfast2BPizza2B5002B296294dcea8a.jpg", "social_rank": 99.99999990783806, "publisher_url": "http://closetcooking.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/46895", "title": "Pepperoni Pizza Burgers", "source_url": "http://thepioneerwoman.com/cooking/2012/10/pepperoni-pizza-burgers/", "recipe_id": "46895", "image_url": "http://static.food2fork.com/pizzaburgera5bd.jpg", "social_rank": 99.99999990525365, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35635", "title": "Thai Chicken Pizza with Sweet Chili Sauce", "source_url": "http://www.closetcooking.com/2012/02/thai-chicken-pizza-with-sweet-chili.html", "recipe_id": "35635", "image_url": "http://static.food2fork.com/Thai2BChicken2BPizza2Bwith2BSweet2BChili2BSauce2B5002B435581bcf578.jpg", "social_rank": 99.99999990065892, "publisher_url": "http://closetcooking.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/47000", "title": "One Basic Pizza Crust", "source_url": "http://thepioneerwoman.com/cooking/2011/09/steakhouse-pizza/", "recipe_id": "47000", "image_url": "http://static.food2fork.com/steakhousepizza0b87.jpg", "social_rank": 99.99999981149679, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "Two Peas and Their Pod", "f2f_url": "http://food2fork.com/view/54491", "title": "Peach, Basil, Mozzarella, & Balsamic Pizza", "source_url": "http://www.twopeasandtheirpod.com/peach-basil-mozzarella-balsamic-pizza/", "recipe_id": "54491", "image_url": "http://static.food2fork.com/peachbasilpizza6c7de.jpg", "social_rank": 99.99999980232263, "publisher_url": "http://www.twopeasandtheirpod.com"}, {"publisher": "Real Simple", "f2f_url": "http://food2fork.com/view/38812", "title": "English-Muffin Egg Pizzas", "source_url": "http://www.realsimple.com/food-recipes/browse-all-recipes/english-muffin-egg-pizzas-10000000663044/index.html", "recipe_id": "38812", "image_url": "http://static.food2fork.com/pizza_300d938bd58.jpg", "social_rank": 99.99999978548222, "publisher_url": "http://realsimple.com"}, {"publisher": "My Baking Addiction", "f2f_url": "http://food2fork.com/view/dd21dd", "title": "Simple No Knead Pizza Dough", "source_url": "http://www.mybakingaddiction.com/no-knead-pizza-dough-recipe/", "recipe_id": "dd21dd", "image_url": "http://static.food2fork.com/PizzaDough1of12edit5779.jpg", "social_rank": 99.9999995838859, "publisher_url": "http://www.mybakingaddiction.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/47011", "title": "Grilled Veggie Pizza", "source_url": "http://thepioneerwoman.com/cooking/2011/07/grilled-vegetable-pizza/", "recipe_id": "47011", "image_url": "http://static.food2fork.com/grilledveggie79bd.jpg", "social_rank": 99.99999947603048, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "My Baking Addiction", "f2f_url": "http://food2fork.com/view/0fb8f4", "title": "Spicy Chicken and Pepper Jack Pizza", "source_url": "http://www.mybakingaddiction.com/spicy-chicken-and-pepper-jack-pizza-recipe/", "recipe_id": "0fb8f4", "image_url": "http://static.food2fork.com/FlatBread21of1a180.jpg", "social_rank": 99.99999927351223, "publisher_url": "http://www.mybakingaddiction.com"}, {"publisher": "All Recipes", "f2f_url": "http://food2fork.com/view/12913", "title": "Exquisite Pizza Sauce", "source_url": "http://allrecipes.com/Recipe/Exquisite-Pizza-Sauce/Detail.aspx", "recipe_id": "12913", "image_url": "http://static.food2fork.com/23868217b6.jpg", "social_rank": 99.99999884376517, "publisher_url": "http://allrecipes.com"}, {"publisher": "Simply Recipes", "f2f_url": "http://food2fork.com/view/36476", "title": "How to Grill Pizza", "source_url": "http://www.simplyrecipes.com/recipes/how_to_grill_pizza/", "recipe_id": "36476", "image_url": "http://static.food2fork.com/howtogrillpizzad300x20086a60e1b.jpg", "social_rank": 99.99999704095504, "publisher_url": "http://simplyrecipes.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/47161", "title": "PW\u2019s Favorite Pizza", "source_url": "http://thepioneerwoman.com/cooking/2010/02/my-favorite-pizza/", "recipe_id": "47161", "image_url": "http://static.food2fork.com/4364270576_302751a2a4f3c1.jpg", "social_rank": 99.99999689667648, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "My Baking Addiction", "f2f_url": "http://food2fork.com/view/a723e8", "title": "Barbecue Chicken Pizza", "source_url": "http://www.mybakingaddiction.com/barbecue-chicken-pizza-recipe/", "recipe_id": "a723e8", "image_url": "http://static.food2fork.com/BBQChickenPizza3e2b.jpg", "social_rank": 99.9999968917598, "publisher_url": "http://www.mybakingaddiction.com"}, {"publisher": "Two Peas and Their Pod", "f2f_url": "http://food2fork.com/view/54388", "title": "Avocado Pita Pizza with Cilantro Sauce", "source_url": "http://www.twopeasandtheirpod.com/avocado-pita-pizza-with-cilantro-sauce/", "recipe_id": "54388", "image_url": "http://static.food2fork.com/avocadopizzawithcilantrosauce4bf5.jpg", "social_rank": 99.99999665701256, "publisher_url": "http://www.twopeasandtheirpod.com"}, {"publisher": "BBC Good Food", "f2f_url": "http://food2fork.com/view/cb13dd", "title": "Pizza margherita in 4 easy steps", "source_url": "http://www.bbcgoodfood.com/recipes/4683/pizza-margherita-in-4-easy-steps", "recipe_id": "cb13dd", "image_url": "http://static.food2fork.com/4683_MEDIUM544c.jpg", "social_rank": 99.99999624664413, "publisher_url": "http://www.bbcgoodfood.com"}, {"publisher": "What's Gaby Cooking", "f2f_url": "http://food2fork.com/view/ead4e0", "title": "Pizza Monkey Bread", "source_url": "http://whatsgabycooking.com/pizza-monkey-bread/", "recipe_id": "ead4e0", "image_url": "http://static.food2fork.com/PizzaMonkeyBread67f8.jpg", "social_rank": 99.99999570141472, "publisher_url": "http://whatsgabycooking.com"}, {"publisher": "The Pioneer Woman", "f2f_url": "http://food2fork.com/view/46892", "title": "Supreme Pizza Burgers", "source_url": "http://thepioneerwoman.com/cooking/2012/10/supreme-pizza-burgers/", "recipe_id": "46892", "image_url": "http://static.food2fork.com/burger53be.jpg", "social_rank": 99.99999283988569, "publisher_url": "http://thepioneerwoman.com"}, {"publisher": "Closet Cooking", "f2f_url": "http://food2fork.com/view/35128", "title": "Balsamic Strawberry and Chicken Pizza with Sweet Onions and Smoked Bacon", "source_url": "http://www.closetcooking.com/2012/07/balsamic-strawberry-and-chicken-pizza.html", "recipe_id": "35128", "image_url": "http://static.food2fork.com/Strawberry2BBalsamic2BPizza2Bwith2BChicken252C2BSweet2BOnion2Band2BSmoked2BBacon2B5002B300939d125e2.jpg", "social_rank": 99.99998682928603, "publisher_url": "http://closetcooking.com"}]}


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
        request.session['shopping_list'].append(request.POST.get('recipe_id'))
