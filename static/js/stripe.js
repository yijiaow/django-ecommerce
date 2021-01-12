// Create a Stripe client
// const stripe = Stripe('{{ STRIPE_PUBLISHABLE_KEY }}');
const stripe = Stripe(
  'pk_test_51Hzo1KD4dlDivOg8aUOej0x0UJBouBOAzvjVzmM2YHQI1e56raqSZtiWghoc8iJYTOXTDbRguylnYP2hDXJUgyj000LSUUpBFj'
);

// Disable submit button until we have Stripe set up on the page
document.querySelector(`button[type='submit']`).disabled = true;
fetch('/payment/create-payment-intent', {
  headers: {
    method: 'POST',
    mode: 'same-origin',
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  },
})
  .then((res) => res.json())
  .then((data) => {
    const elements = stripe.elements();

    var style = {
      base: {
        color: '#32325d',
        fontFamily: 'Arial, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#32325d',
        },
      },
      invalid: {
        fontFamily: 'Arial, sans-serif',
        color: '#fa755a',
        iconColor: '#fa755a',
      },
    };

    // Create an instance of the card Element
    const card = elements.create('card', { style: style });

    // // Stripe injects an iframe into the DOM
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element
    card.on('change', (event) => {
      // Disable the Pay button if there are no card details in the Element
      document.querySelector(`button[type='submit']`).disabled = event.empty;
      document.querySelector('#card-error').textContent = event.error
        ? event.error.message
        : '';
    });

    const form = document.getElementById('stripe-payment-form');
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      // Complete payment when submit button is clicked
      payWithCard(stripe, card, data.client_secret);
    });
  });

const payWithCard = (stripe, card, client_secret) => {
  loading(true);
  stripe
    .confirmCardPayment(client_secret, {
      payment_method: {
        card: card,
      },
    })
    .then((res) => {
      if (res.error) {
        showError(res.error.message);
      } else {
        orderComplete(res.paymentIntent.id);
      }
    });
};

/* ------- UI helpers ------- */

// Show a success message when payment is complete
const orderComplete = (paymentIntentId) => {
  loading(false);
  document
    .querySelector('.result-message a')
    .setAttribute(
      'href',
      `https://dashboard.stripe.com/test/payments/${paymentIntentId}`
    );
  document.querySelector('.result-message').classList.remove('hidden');
  document.querySelector(`button[type='submit']`).disabled = true;
};

// Show customer the error from Stripe if the card fails to charge
const showError = (errorMsg) => {
  loading(false);
  document.querySelector('#card-error').textContent = errorMsg;
};

// Show a spinner on payment submission
const loading = (isLoading) => {
  if (isLoading) {
    // Disable submit button and show a spinner
    document.querySelector(`button[type='submit']`).disabled = true;
    document.querySelector('#spinner').classList.remove('hidden');
    document.querySelector('#btn-text').classList.add('hidden');
  } else {
    document.querySelector(`button[type='submit']`).disabled = false;
    document.querySelector('#spinner').classList.add('hidden');
    document.querySelector('#btn-text').classList.remove('hidden');
  }
};
