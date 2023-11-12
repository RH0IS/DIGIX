# coinmarketapp/views.py
import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import CryptoCurrency

def crypto_list(request):
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


def demo(request):
    return render(request,'coinmarketapp/demo-page.html')

def error(request):
    return render(request, 'coinmarketapp/error.html')


def get_exchange_rate(request, from_currency):
    try:
        # Define your API key (replace with your actual API key)
        api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

        # Define headers with your API key
        headers = {
            'X-CMC_PRO_API_KEY': api_key,
        }

        # Make the API request
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Return the response to the frontend
        return JsonResponse(response.json())

    except requests.exceptions.HTTPError as errh:
        return JsonResponse({'error': f"HTTP Error: {errh}"}, status=500)

    except requests.exceptions.ConnectionError as errc:
        return JsonResponse({'error': f"Error Connecting: {errc}"}, status=500)

    except requests.exceptions.Timeout as errt:
        return JsonResponse({'error': f"Timeout Error: {errt}"}, status=500)

    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"Something went wrong: {err}"}, status=500)


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
        return render(request, 'coinmarketapp/trends.html', {'cryptocurrencies': cryptocurrencies})
    else:
        # Handle API request error
        return render(request, 'coinmarketapp/error.html')


def exchange(request):
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
    currency = []
    for crypto in data['data']:
        name = crypto['name']
        currency.append(name)

    return render(request, 'coinmarketapp/exchange.html', {'name': currency})