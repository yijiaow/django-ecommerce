from django import forms

from .widgets import NumberStepperWidget


class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        required=False, initial=1, label='', widget=NumberStepperWidget(attrs={'min': 1, 'max': 10}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'street_address_line1', 'street_address_line2',
                  'city', 'state', 'country', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class ShippingForm(AddressForm):
    email = forms.EmailField(required=False)
    use_default_shipping = forms.BooleanField(
        required=False, initial=True, label='Use default shipping address')
    set_as_default = forms.BooleanField(
        required=False, initial=True, label='Save as default shipping address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['use_default_shipping'].widget.attrs['class'] = 'form-control-input'


class BillingForm(AddressForm):
    same_as_shipping = forms.BooleanField(
        required=False, initial=True, label='Billing address is the same as shipping address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['same_as_shipping'].widget.attrs['class'] = 'form-control-input'
