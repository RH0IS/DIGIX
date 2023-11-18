# coinmarketapp/views.py
import requests
from django.http import JsonResponse
from django.shortcuts import render
from .models import CryptoCurrency

def get_exchange_rates(request):
    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key,
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()

    return JsonResponse(data)

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


def get_exchange_rate(request, from_currency, to_currency):
    try:
        # Replace this with your actual CoinMarketCap API key
        coinmarketcap_api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

        # Define headers with your CoinMarketCap API key
        headers = {
            'X-CMC_PRO_API_KEY': coinmarketcap_api_key,
        }

        # Define parameters for the CoinMarketCap API request
        params = {
            'start': 1,  # Starting record
            'limit': 10,  # Number of cryptocurrencies to retrieve
            'convert': to_currency,  # Convert prices to the target currency
        }

        # Make the CoinMarketCap API request
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        response_json = response.json()

        # Check if 'data' is present in the response
        if 'data' in response_json:
            data = response_json['data']

            # Find the requested cryptocurrency in the response
            crypto_info = next((crypto for crypto in data if crypto['symbol'] == from_currency), None)

            if crypto_info:
                # Extract the price in the target currency
                price = crypto_info['quote'][to_currency]['price']

                return JsonResponse({'rate': price})

            else:
                return JsonResponse({'error': f'Cryptocurrency with symbol {from_currency} not found'}, status=400)

        else:
            return JsonResponse({'error': 'Failed to fetch cryptocurrency data'}, status=500)

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

    try:
        # Make the API request
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract relevant information
            cryptocurrencies = []
            for crypto in data['data']:
                name = crypto['name']
                symbol = crypto['symbol']
                price = crypto['quote']['USD']['price']

                cryptocurrency = {
                    'name': name,
                    'symbol': symbol,
                    'price': price,
                }

                cryptocurrencies.append(cryptocurrency)

            return render(request, 'coinmarketapp/currency_converter.html', {'cryptocurrencies': cryptocurrencies})

        else:
            return JsonResponse({'error': 'Failed to fetch cryptocurrency data'}, status=response.status_code)

    except requests.exceptions.RequestException as err:
        return JsonResponse({'error': f"Something went wrong: {err}"}, status=500)