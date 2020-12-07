from django import forms


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(required=True)
