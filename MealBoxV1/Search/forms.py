from django import forms


class SearchForm(forms.Form):
    your_name = forms.CharField(label='search', max_length=100)