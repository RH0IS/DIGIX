# coinmarketapp/views.py
import json
import requests
import stripe
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import CryptoCurrency
from .forms import RowSelectionForm, OrderForm

stripe.api_key = 'sk_test_51O4pjuHl9Bqmml9jt2gupSLgAY6JjnvhQ9YaHuNHWZJOZZVZdeZHD67aG6WOkxXxIyy7OBQQKNdrWH90U3qaAVhO00tHqCFiRH'


def crypto_list(request):
    # Define the CoinMarketCap API URL
    form = RowSelectionForm(request.GET or None)
    number_of_rows = 10

    if form.is_valid():
        number_of_rows = form.cleaned_data['number_of_rows']
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # Define your API key (replace with your actual CoinMarketCap API key)
    api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

    # Define parameters for the API request
    params = {
        'start': 1,  # Starting record
        'limit': number_of_rows,  # Number of cryptocurrencies to retrieve
        'convert': 'USD',  # Convert prices to USD
    }

    # Define headers with your API key
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
    }

    # Make the API request
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant data from the API response
        CryptoCurrency.objects.all().delete()

        for crypto in data['data']:
            name = crypto['name']
            symbol = crypto['symbol']
            market_cap = crypto['quote']['USD']['market_cap']
            price = crypto['quote']['USD']['price']
            volume_24h = crypto['quote']['USD']['percent_change_1h']

            crypto_obj = CryptoCurrency(
                name=name,
                symbol=symbol,
                market_cap=market_cap,
                price=price,
                volume_24h=volume_24h
            )
            crypto_obj.save()

        # Pass the cryptocurrency data to the template
        cryptocurrencies = CryptoCurrency.objects.all()
        return render(request, 'coinmarketapp/crypto_list.html', {
            'cryptocurrencies': cryptocurrencies,
            'form': form
        })
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')


def demo(request):
    return render(request, 'coinmarketapp/demo-page.html')


def error(request):
    return render(request, 'coinmarketapp/error.html')


def trends_view(request):
    # Define the CoinMarketCap API URL
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # Define your API key (replace with your actual CoinMarketCap API key)
    api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

    # Define parameters for the API request
    params = {
        'start': 1,  # Starting record
        'limit': 10,  # Number of cryptocurrencies to retrieve
        'convert': 'USD',  # Convert prices to USD
    }

    # Define headers with your API key
    headers = {
        'X-CMC_PRO_API_KEY': api_key,
    }

    # Make the API request
    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant data from the API response
        cryptocurrencies = []
        for crypto in data['data']:
            name = crypto['name']
            symbol = crypto['symbol']
            market_cap = crypto['quote']['USD']['market_cap']
            price = crypto['quote']['USD']['price']
            volume_24h = crypto['quote']['USD']['volume_change_24h']

            crypto_obj = CryptoCurrency(
                name=name,
                symbol=symbol,
                market_cap=market_cap,
                price=price,
                volume_24h=volume_24h
            )
            cryptocurrencies.append(crypto_obj)

        # Pass the cryptocurrency data to the template
        return render(request, 'coinmarketapp/trends.html', {'cryptocurrencies': cryptocurrencies})
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')


@login_required
def render_payment_page(request) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        if form.is_valid():
            try:
                unit_price = CryptoCurrency.objects.get(id=form.cleaned_data['crypto_currency'].id).price
                order = form.save(commit=False)
                order.amount = int(form.cleaned_data['crypto_amount'] * unit_price * 100)
                if order.amount <= 0:
                    raise Exception('the price should be more than 0')
                order.currency = 'cad'
                order.user = request.user
                order.email = form.cleaned_data['email']
                order.save()
                # Create a PaymentIntent with the order amount and currency
                intent = stripe.PaymentIntent.create(
                    amount=order.amount,
                    currency='cad',
                    automatic_payment_methods={'enabled': True, },
                )
                return render(request, 'coinmarketapp/checkout.html', {
                    'clientSecret': intent['client_secret'],
                    'url': 'http://' + request.get_host() + '/pay-result',
                    'email': order.email
                })
            except Exception as e:
                messages.error(request, e)
                return HttpResponse("fail to create order")
    form = OrderForm()
    form.set(email=request.user.email)
    return render(request, 'coinmarketapp/create_order.html', {'form': form})


@login_required
def pay_reslut(request):
    is_success = request.GET.get('redirect_status')
    if is_success == 'succeeded':
        print(request.GET.get('payment_intent'))
        print(request.GET.get('payment_intent_client_secret'))
    else:
        print('PaymentIntent faild: {}'.format(is_success))
    return render(request, 'coinmarketapp/return.html')


@login_required
def user_profile(request):
    # user_wallet = UserWallet.objects.get_or_create(user=request.user)[0]
    # cryptocurrencies = user_wallet.currencies.all()
    return render(request, 'coinmarketapp/user_profile.html')
    # return render(request, 'coinmarketapp/user_profile.html',
    #               {'user_wallet': user_wallet, 'cryptocurrencies': cryptocurrencies})
