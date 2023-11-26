# coinmarketapp/views.py
import json
import requests
import stripe
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .models import CryptoCurrency, UserWallet, trending_crypto
from .forms import RowSelectionForm

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'

def ticker_base(request):
    trending_api_url = "https://api.coingecko.com/api/v3/coins/markets"

    # Define parameters for the API request
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 3,
        'page': 1,
        'sparkline': False,
        'locale': 'en'
    }

    # Make the API request
    response = requests.get(trending_api_url, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant data from the API response
        trending_currencies = []

        for crypto in data:
            name = crypto['name']
            symbol = crypto['symbol']
            rank = crypto['market_cap_rank']
            price_change_percentage_24h = crypto['price_change_percentage_24h']
            image = crypto['image']

            # Create a trending_crypto object
            trending_obj = trending_crypto(
                name=name,
                symbol=symbol,
                rank=rank,
                price_change_percentage_24h=price_change_percentage_24h,
                image=image
            )
            # Save the object to the database
            trending_obj.save()
            trending_currencies.append(trending_obj)

        # Additional data or functionality
        total_cryptos = len(trending_currencies)
        highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
        lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)

        # Pass the cryptocurrency data and additional data to the template
        return render(request, 'coinmarketapp/base.html', {
                                                             'trending_currencies': trending_currencies,
                                                             'total_cryptos': total_cryptos,
                                                             'highest_ranked_crypto': highest_ranked_crypto,
                                                             'lowest_ranked_crypto': lowest_ranked_crypto
                                                             })
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
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

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def demo(request):
    trending_api_url = "https://api.coingecko.com/api/v3/coins/markets"

    # Define parameters for the API request
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 3,
        'page': 1,
        'sparkline': False,
        'locale': 'en'
    }

    # Make the API request
    response = requests.get(trending_api_url, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant data from the API response
        trending_currencies = []

        for crypto in data:
            name = crypto['name']
            symbol = crypto['symbol']
            rank = crypto['market_cap_rank']
            price_change_percentage_24h = crypto['price_change_percentage_24h']
            image = crypto['image']

            # Create a trending_crypto object
            trending_obj = trending_crypto(
                name=name,
                symbol=symbol,
                rank=rank,
                price_change_percentage_24h=price_change_percentage_24h,
                image=image
            )
            # Save the object to the database
            trending_obj.save()
            trending_currencies.append(trending_obj)

        # Additional data or functionality
        total_cryptos = len(trending_currencies)
        highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
        lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)

        # Pass the cryptocurrency data and additional data to the template
        return render(request, 'coinmarketapp/demo-page.html', {
            'trending_currencies': trending_currencies,
            'total_cryptos': total_cryptos,
            'highest_ranked_crypto': highest_ranked_crypto,
            'lowest_ranked_crypto': lowest_ranked_crypto
        })
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')
    # return render(request, 'coinmarketapp/demo-page.html')


def error(request):
    return render(request, 'coinmarketapp/error.html')

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def trends_view(request):
    form = RowSelectionForm(request.GET or None)
    number_of_rows = 10

    if form.is_valid():
        number_of_rows = form.cleaned_data['number_of_rows']
    market_api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

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
    response = requests.get(market_api_url, params=params, headers=headers)

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
    # Define the CoinGecko API URL
    trending_api_url = "https://api.coingecko.com/api/v3/coins/markets"

    # Define parameters for the API request
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 3,
        'page': 1,
        'sparkline': False,
        'locale': 'en'
    }

    # Make the API request
    response = requests.get(trending_api_url, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant data from the API response
        trending_currencies = []

        for crypto in data:
            name = crypto['name']
            symbol = crypto['symbol']
            rank = crypto['market_cap_rank']
            price_change_percentage_24h = crypto['price_change_percentage_24h']
            image = crypto['image']

            # Create a trending_crypto object
            trending_obj = trending_crypto(
                name=name,
                symbol=symbol,
                rank=rank,
                price_change_percentage_24h=price_change_percentage_24h,
                image=image
            )
            # Save the object to the database
            trending_obj.save()
            trending_currencies.append(trending_obj)

        # Additional data or functionality
        total_cryptos = len(trending_currencies)
        highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
        lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)

        # Pass the cryptocurrency data and additional data to the template
        return render(request, 'coinmarketapp/trends.html', {'cryptocurrencies':cryptocurrencies,
            'trending_currencies': trending_currencies,
            'total_cryptos': total_cryptos,
            'highest_ranked_crypto': highest_ranked_crypto,
            'lowest_ranked_crypto': lowest_ranked_crypto
        })
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