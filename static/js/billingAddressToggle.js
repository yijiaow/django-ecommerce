const hideable_billing_form = document.querySelector('.hideable-billing-form');
const hideable_shipping_address = document.getElementById('hideable-shipping-address')

const same_as_shipping = document.querySelector(
  `input[name='same_as_shipping']`
);

same_as_shipping.addEventListener('change', (e) => {
  if (e.currentTarget.checked) {
    hideable_billing_form.hidden = true;
    hideable_shipping_address.hidden = false
  } else {
    hideable_billing_form.hidden = false;
    hideable_shipping_address.hidden = true
  }
});
