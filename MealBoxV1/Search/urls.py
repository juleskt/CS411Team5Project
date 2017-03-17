from django.conf.urls import url

urlpatterns = [
    url(r'^search', 'Search.views.get_name', name='search_page'),
]