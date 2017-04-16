from django.shortcuts import render

def index(request):
    recipeList = []
    if 'shopping_list' not in request.session:
        request.session['shopping_list'] = []
    for recipe in request.session['shopping_list']:
        recipeList.append(searchDBForRecipe(recipe))
    return render(request, 'cart.html', {'recipes': recipeList})