from django import forms
from .models import Search


class SearchForm(forms.Form):
    your_name = forms.CharField(label='search', max_length=100)