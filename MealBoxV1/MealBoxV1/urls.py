"""MealBoxV1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django import http

from Search import views as SearchViews
from Login import views as LoginViews
from Recipes import views as RecipesViews
from ShoppingList import views as ListViews
from Cart import views as CartViews


def session_test_1(request):
    request.session['test'] = 'Session Vars Worked!'
    return http.HttpResponseRedirect('done/?session=%s' % request.session.session_key)


def session_test_2(request):
    return http.HttpResponse('<br>'.join([
        request.session.session_key,
        request.GET.get('session'),
        request.session.get('test', 'Session is Borked :(')
    ]))

urlpatterns = [
    url(r'^$', LoginViews.index, name='index'),
    url(r'^$', LoginViews.handleLogout, name='logout'),
    url(r'^handleLogin/$', LoginViews.handleLogin, name='handleLogin'),
    url(r'^admin/', admin.site.urls),
    url(r'^contact/$', SearchViews.contact, name='contact'),
    url(r'^search/$', SearchViews.search, name='search'),
    url(r'^search-result/$', SearchViews.search, name='search-result'),
    url(r'^add-recipe', SearchViews.addRecipe, name='add-recipe'),
    url(r'^delete-recipe', RecipesViews.deleteRecipe, name='delete-recipe'),
    url(r'^shopping-list-from-search/$', SearchViews.addToShoppingList, name='add-to-shopping-list'),
    url(r'^my-recipes/$', RecipesViews.showrecipes, name='my-recipes'),
    url(r'^my-shopping-list/$', ListViews.index, name='my-list'),
    url(r'^remove-from-list/$', ListViews.removeFromList, name='remove-from-list'),
    url(r'^quick-add-to-cart/$', ListViews.quickAddToCart, name='quick-add-to-cart'),
    url(r'^get-amazon-results/$', ListViews.getAmazonResultsForModal, name='lookup-ingredients-amazon'),
    url(r'^add-to-amazon-cart/$', ListViews.addToAmazonCart, name='add-to-amazon-cart'),
    url(r'^addtocart/$', CartViews.addtocart, name='add-to-cart'),
    url(r'^remove-from-cart/$', CartViews.removefromcart, name='remove-from-cart'),
    url(r'^cart/$', CartViews.index, name='cart'),

    #url(r'^session-test/$', session_test_1),
    #url(r'^session-test/done/$', session_test_2),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
