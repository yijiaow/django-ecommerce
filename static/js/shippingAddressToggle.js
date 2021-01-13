const hideable_shipping_form = document.querySelector(
  '.hideable-shipping-form'
);
const hideable_shipping_address = document.getElementById(
  'hideable-shipping-address'
);

const use_default_shipping = document.querySelector(
  `input[name='use_default_shipping']`
);

use_default_shipping.addEventListener('change', (e) => {
  if (e.currentTarget.checked) {
    hideable_shipping_form.hidden = true;
    hideable_shipping_address.hidden = false;
  } else {
    hideable_shipping_form.hidden = false;
    hideable_shipping_address.hidden = true;
  }
});
