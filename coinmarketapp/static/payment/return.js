initialize();

async function initialize() {
    const stripe = Stripe('pk_test_A7jK4iCYHL045qgjjfzAfPxu');
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const redirect_status = urlParams.get('redirect_status');
    const payment_intent = urlParams.get('payment_intent');
    const clientSecret = urlParams.get('payment_intent_client_secret');
    stripe.retrievePaymentIntent(clientSecret).then(({paymentIntent}) => {
        const message = document.querySelector('#message')
        // Inspect the PaymentIntent `status` to indicate the status of the payment
        // to your customer.
        //
        // Some payment methods will [immediately succeed or fail][0] upon
        // confirmation, while others will first enter a `processing` state.
        //
        // [0]: https://stripe.com/docs/payments/payment-methods#payment-notification
        console.log(paymentIntent)
        switch (paymentIntent.status) {
            case 'succeeded':
                message.innerText = 'Success! Payment received(Paid ' + paymentIntent.amount + paymentIntent.currency + ').';
                break;

            case 'processing':
                message.innerText = "Payment processing. We'll update you when payment is received.";
                break;

            case 'requires_payment_method':
                message.innerText = 'Payment failed. Please try another payment method.';
                // Redirect your user back to your payment page to attempt collecting
                // payment again
                break;

            default:
                message.innerText = 'Something went wrong.';
                break;
        }
    });
    // const response = await fetch(`/session-status?session_id=${sessionId}`);
    // const session = await response.json();
    //
    // if (session.status == 'open') {
    //     window.replace('http://localhost:4242/checkout.html')
    // } else if (session.status == 'complete') {
    //     document.getElementById('success').classList.remove('hidden');
    //     document.getElementById('customer-email').textContent = session.customer_email
    // }
}