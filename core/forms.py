from django import forms

from .widgets import NumberStepperWidget


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        required=False, initial=1, label='', widget=NumberStepperWidget(attrs={'min': 1, 'max': 10}))


class BillingForm(AddressForm):
    same_as_shipping = forms.BooleanField(
        required=False, initial=True, label='Billing address is the same as shipping address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['same_as_shipping'].widget.attrs['class'] = 'form-control-input'
