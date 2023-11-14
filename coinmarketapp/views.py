# coinmarketapp/views.py
import json
import requests
import stripe
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import CryptoCurrency, UserWallet
from .forms import RowSelectionForm

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'


@login_required(login_url='login')  
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
        return render(request, 'coinmarketapp/crypto_list.html', {'cryptocurrencies': cryptocurrencies,
                                                                  'form':form
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


@csrf_exempt
def create_payment(request):
    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=1400,
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return HttpResponse(json.dumps({'clientSecret': intent['client_secret']}), content_type='application/json')
        # return jsonify({
        #     'clientSecret': intent['client_secret']
        # })
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'code': '400', 'msg': 'fail'}), content_type='application/json')


def payment_result(request):
    return render(request, 'coinmarketapp/return.html')


# Create your views here.
def payment_test(request) -> HttpResponse:
    return render(request, 'coinmarketapp/checkout.html')
@login_required
def user_profile(request):
    user_wallet = UserWallet.objects.get_or_create(user=request.user)[0]
    cryptocurrencies = user_wallet.currencies.all()
    return render(request, 'coinmarketapp/user_profile.html', {'user_wallet': user_wallet, 'cryptocurrencies': cryptocurrencies})