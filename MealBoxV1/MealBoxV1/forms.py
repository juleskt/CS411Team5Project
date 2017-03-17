# make sure this is at the top if it isn't already
from django import forms


# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class SearchForm(forms.Form):
  search = forms.CharField(required=True)