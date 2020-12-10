from django import forms

from .widgets import NumberStepperWidget


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        required=False, initial=1, label='', widget=NumberStepperWidget(attrs={'min': 1, 'max': 10}))
