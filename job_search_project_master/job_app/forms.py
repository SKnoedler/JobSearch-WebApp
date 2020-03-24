from django import forms
from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.layout import Field


class FormsetForm(forms.Form):
    delete= forms.BooleanField(required=False, initial=False)
    # some other fields with data



class SearchForm(forms.Form):

    fields = ('search_term', 'location')# 'firm_undesired1', 'firm_undesired2', 'firm_undesired3', 'firm_undesired4', 'firm_undesired5','title_undesired1', 'title_undesired2', 'title_undesired3', 'title_undesired4', 'title_undesired5', 'title_desired1','title_desired2', 'title_desired3', 'title_desired4', 'title_desired5')

    labels = {
        'search_term': '',
        'location': ''
    }

    def __init__(self, *args, **kwargs): #arguments parameter and keyword parameter
        self.fields['search_term'].widget.attrs['placeholder'] = 'Job Titles, Companies or technology'
        self.fields['location'].widget.attrs['placeholder'] = 'e.g. Frankfurt am Main'