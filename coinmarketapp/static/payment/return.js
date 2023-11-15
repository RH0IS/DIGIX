const stripe = Stripe("pk_test_51O4pjuHl9Bqmml9jPpA17vmslVW141KmpRfae2j5Yg1VdOBlleiuO9jtM3QSvmkesgvxVb3b5L9v5jaPsJlyOSfc00HUdEXorn");

initialize();

async function initialize() {
    stripe.retrievePaymentIntent(new URLSearchParams(window.location.search).get("payment_intent_client_secret")).then((res) => {
        const message = document.querySelector('#message')
        message.classList.remove('hidden')
        console.log('res', res)
        if (res.paymentIntent) {
            let data = res.paymentIntent
            switch (data.status) {
                case 'succeeded':
                    message.innerText = 'We appreciate your business! You can close this page now.'
                    message.innerText += '\n' + 'Transaction ID: ' + data.id + '. Paid ' + data.amount + res.paymentIntent.currency + '.'
                    message.innerText += ' A confirmation email will be sent to ' + data.receipt_email + ' .'
                    break;
                case 'processing':
                    message.innerText = "Payment processing. We'll update you when payment is received. You can close this page now.";
                    break;

                case 'requires_payment_method':
                    message.innerText = 'Payment failed. Please try another payment method.';
                    break;

                default:
                    message.innerText = 'Something went wrong.';
                    break;
            }
        } else if (res.error) {
            message.innerText = 'Something went wrong, here are some information that might help: ' + res.error.message;
        } else {
            message.innerText = 'Something went wrong.';
        }
    });
}