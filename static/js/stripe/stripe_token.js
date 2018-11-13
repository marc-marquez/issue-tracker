/* Event listener code used according to spec from https://stripe.com/docs/stripe-js/reference */
var stripe = Stripe('pk_test_BfDz5kfXdE0xApIu8HYMfWEQ');
var elements = stripe.elements();
var style = {
  base: {
    fontSize: '16px',
    color: "#32325d",
  }
};

var card = elements.create('card',{style: style});
card.mount('#card-element');

card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = document.getElementById('card-form');
form.addEventListener('submit', function(event) {

  event.preventDefault();

  //Check if customer exists, if not create a new customer

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the customer that there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('card-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}