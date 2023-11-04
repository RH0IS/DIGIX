# coinmarketapp/views.py
import requests
from django.shortcuts import render
from .models import CryptoCurrency

def crypto_list(request):
    # Define the CoinMarketCap API URL
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    # Define your API key (replace with your actual CoinMarketCap API key)
    api_key = "Y1400ea97-a782-4685-81f3-d9ad1ef83928"

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
            volume_24h = crypto['quote']['USD']['volume_24h']

            crypto_obj = CryptoCurrency(
                name=name,
                symbol=symbol,
                market_cap=market_cap,
                price=price,
                volume_24h=volume_24h
            )
            cryptocurrencies.append(crypto_obj)

        # Pass the cryptocurrency data to the template
        return render(request, 'coinmarketapp/crypto_list.html', {'cryptocurrencies': cryptocurrencies})
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')


# def index(request):
#     data = {}
#     data["crypto_data"] = get_crypto_data()
#     return render(request, "myappF23/index.html", context=data)
#
#
# # return the data received from api as json object
# def get_crypto_data():
#     # api_url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
#     api_url = "http://api.coinlayer.com/live?access_key=cc193be204150f270335cb8652f14683"
#     try:
#         data = requests.get(api_url).json()
#
#     except Exception as e:
#         print(e)
#         data = dict()
#     #rates = data['rates']
#     return data