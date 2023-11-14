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
        message.classList.remove('hidden')
        console.log(paymentIntent)
        switch (paymentIntent.status) {
            case 'succeeded':
                message.innerText = 'We appreciate your business!';
                document.getElementById('customer-email').textContent = session.customer_email
                //  Payment received(Paid ' + paymentIntent.amount + paymentIntent.currency + ').
                break;

            case 'processing':
                message.innerText = "Payment processing. We'll update you when payment is received. You can close this page now.";
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