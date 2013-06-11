# NOT IN USE

from django import forms
from .models import InvoiceLine


class InvoiceInlineForm (forms.ModelForm):
    foo = forms.CharField ('Foo Fighters')
    bar = forms.CharField ('Barbarosa')
#    class Meta:
#        model = InvoiceLine
