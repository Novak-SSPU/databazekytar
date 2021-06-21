from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Type, Guitar


class GuitarModelForm(ModelForm):
    def clean_runtime(self):
       data = self.cleaned_data['stringnumber']
       if data <= 0 or data > 1000:
           raise ValidationError('Neplatná délka kytar')
       return data

    def clean_rate(self):
       data = self.cleaned_data['rate']
       if data < 1 or data > 10:
           raise ValidationError('Neplatné hodnocení: musí být v rozsahu 1-10')
       return data

    class Meta:
        model = Guitar
        fields = ['name', 'description', 'image', 'image', 'stringnumber', 'rate']
        labels = {'name': 'Název kytary', 'description': 'Popis kytary'}
