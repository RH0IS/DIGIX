# coinmarketapp/views.py
import json
import requests
import stripe
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from .models import CryptoCurrency, UserWallet, Order, trending_crypto
from .forms import RowSelectionForm, OrderForm, ChangeProfilePictureForm, SellForm
from django.shortcuts import get_object_or_404
from authentication.models import UserProfile
from django.core.exceptions import ValidationError


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


stripe.api_key = "sk_test_51O4pjuHl9Bqmml9jt2gupSLgAY6JjnvhQ9YaHuNHWZJOZZVZdeZHD67aG6WOkxXxIyy7OBQQKNdrWH90U3qaAVhO00tHqCFiRH"


def __update_crypto_currency(data) -> None:
    for crypto in data["data"]:
        name = crypto["name"]
        symbol = crypto["symbol"]
        market_cap = crypto["quote"]["USD"]["market_cap"]
        price = crypto["quote"]["USD"]["price"]
        volume_24h = crypto["quote"]["USD"][
            "percent_change_1h"
        ]  # Verify the correct key
        CryptoCurrency.objects.update_or_create(
            name=name,
            defaults={
                "name": name,
                "symbol": symbol,
                "market_cap": market_cap,
                "price": price,
                "volume_24h": volume_24h,
            },
        )


@api_view(["GET"])
@throttle_classes([UserRateThrottle])
def crypto_list(request):
    form = RowSelectionForm(request.GET or None)

    if form.is_valid():
        number_of_rows = form.cleaned_data["number_of_rows"]
    else:
        number_of_rows = 10

    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

    params = {
        "start": 1,
        "limit": number_of_rows,
        "convert": "USD",
    }

    headers = {
        "X-CMC_PRO_API_KEY": api_key,
    }

    response = requests.get(api_url, params=params, headers=headers)

    if response.status_code == 200:
        __update_crypto_currency(response.json())

        search_query = request.GET.get("search")
        if search_query:
            cryptocurrencies = CryptoCurrency.objects.filter(
                name__icontains=search_query
            )
        else:
            cryptocurrencies = CryptoCurrency.objects.all()

        return render(
            request,
            "coinmarketapp/crypto_list.html",
            {
                "cryptocurrencies": cryptocurrencies,
                "form": form,
                "search_query": search_query,
            },
        )
    else:
        return render(request, "coinmarketapp/error.html")


def top_crypto_list(request):
    crypto_visits = {}  # Dictionary to store crypto visit counts

    # Loop through cookies to gather visit counts for each crypto
    for key, value in request.COOKIES.items():
        if key != 'csrftoken':  # Exclude CSRF token
            try:
                crypto_visits[key] = int(value)
            except ValueError:
                # Handle the case where the value is not an integer
                crypto_visits[key] = 0

    # Sort crypto_visits by visit count in descending order
    sorted_crypto_visits = sorted(crypto_visits.items(), key=lambda x: x[1], reverse=True)

    # Retrieve CryptoCurrency objects based on sorted crypto names
    top_crypto_list = []
    for crypto_name, _ in sorted_crypto_visits:
        try:
            crypto = CryptoCurrency.objects.get(symbol=crypto_name)
            top_crypto_list.append(crypto)
        except CryptoCurrency.DoesNotExist:
            pass  # Handle case where CryptoCurrency doesn't exist for the given name

    # Render the top crypto list in a template
    return top_crypto_list


def cypto_by_name(request, currname):
    crypto_by_name = CryptoCurrency.objects.get(name=currname)
    symbol = crypto_by_name.symbol
    cookie = request.COOKIES.get(symbol)
    # print(symbol)
    clist = top_crypto_list(request)
    trending_currencies = trending_crypto.objects.all()
    tlist = trending_currencies[:3]
    total_cryptos = len(trending_currencies)
    highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
    lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)
    response = render(request, 'coinmarketapp/crypto_page.html', {
        "cpt": crypto_by_name,
        "clist": clist,
        "trending_currencies": tlist,
        "total_cryptos": total_cryptos,
        "highest_ranked_crypto": highest_ranked_crypto,
        "lowest_ranked_crypto": lowest_ranked_crypto,
    })
    if not cookie:
        response.set_cookie(symbol, '1')
    else:
        cookie = int(cookie) + 1
        response.set_cookie(symbol, cookie)
    # print(clist)
    return response


@api_view(["GET"])
@throttle_classes([UserRateThrottle])
def demo(request):
    trending_api_url = "https://api.coingecko.com/api/v3/coins/markets"

    # Define parameters for the API request
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
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
            name = crypto["name"]
            symbol = crypto["symbol"]
            rank = crypto["market_cap_rank"]
            price_change_percentage_24h = crypto["price_change_percentage_24h"]
            image = crypto["image"]

            # Create a trending_crypto object
            trending_obj = trending_crypto(
                name=name,
                symbol=symbol,
                rank=rank,
                price_change_percentage_24h=price_change_percentage_24h,
                image=image,
            )
            # Save the object to the database
            trending_obj.save()
            trending_currencies.append(trending_obj)

        # Additional data or functionality
        total_cryptos = len(trending_currencies)
        highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
        lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)

        # Pass the cryptocurrency data and additional data to the template
        return render(
            request,
            "coinmarketapp/demo-page.html",
            {
                "trending_currencies": trending_currencies,
                "total_cryptos": total_cryptos,
                "highest_ranked_crypto": highest_ranked_crypto,
                "lowest_ranked_crypto": lowest_ranked_crypto,
            },
        )
    else:
        # Handle API request error
        return render(request, "coinmarketapp/error.html")
    # return render(request, 'coinmarketapp/demo-page.html')


def error(request):
    return render(request, "coinmarketapp/error.html")


@api_view(["GET"])
@throttle_classes([UserRateThrottle])
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
    form = RowSelectionForm(request.GET or None)
    number_of_rows = 10

    if form.is_valid():
        number_of_rows = form.cleaned_data["number_of_rows"]

    market_api_url = (
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    )

    # Define your API key (replace with your actual CoinMarketCap API key)
    api_key = "1400ea97-a782-4685-81f3-d9ad1ef83928"

    # Define parameters for the API request
    params = {
        "start": 1,  # Starting record
        "limit": number_of_rows,  # Number of cryptocurrencies to retrieve
        "convert": "USD",  # Convert prices to USD
    }

    # Define headers with your API key
    headers = {
        "X-CMC_PRO_API_KEY": api_key,
    }

    # Make the API request
    response = requests.get(market_api_url, params=params, headers=headers)

    if response.status_code == 200:
        __update_crypto_currency(response.json())
        # Pass the cryptocurrency data to the template
        cryptocurrencies = CryptoCurrency.objects.all()
    # Define the CoinGecko API URL
    trending_api_url = "https://api.coingecko.com/api/v3/coins/markets"

    # Define parameters for the API request
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 3,
        "page": 1,
        "sparkline": False,
        "locale": "en",
    }

    # Make the API request
    response = requests.get(trending_api_url, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract relevant data from the API response
        trending_currencies = []

        for crypto in data:
            name = crypto["name"]
            symbol = crypto["symbol"]
            rank = crypto["market_cap_rank"]
            price_change_percentage_24h = crypto["price_change_percentage_24h"]
            image = crypto["image"]

            # Create a trending_crypto object
            trending_obj = trending_crypto(
                name=name,
                symbol=symbol,
                rank=rank,
                price_change_percentage_24h=price_change_percentage_24h,
                image=image,
            )
            # Save the object to the database
            trending_obj.save()
            trending_currencies.append(trending_obj)

        # Additional data or functionality
        total_cryptos = len(trending_currencies)
        highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
        lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)
        search_query = request.GET.get("search")
        if search_query:
            cryptocurrencies = CryptoCurrency.objects.filter(
                name__icontains=search_query
            )
        else:
            cryptocurrencies = CryptoCurrency.objects.all()
        # Pass the cryptocurrency data and additional data to the template
        return render(
            request,
            "coinmarketapp/trends.html",
            {
                "cryptocurrencies": cryptocurrencies,
                "trending_currencies": trending_currencies,
                "total_cryptos": total_cryptos,
                "highest_ranked_crypto": highest_ranked_crypto,
                "lowest_ranked_crypto": lowest_ranked_crypto,
                "form": form,
                "search_query": search_query,
            },
        )
    else:
        # Handle API request error
        return render(request, "coinmarketapp/error.html")


@login_required
def render_payment_page(request) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            try:
                if request.user.email is not None:
                    user = get_object_or_404(User, pk=request.user.id)
                    user.email = form.cleaned_data["email"]
                    user.save()
                unit_price = CryptoCurrency.objects.get(
                    id=form.cleaned_data["crypto_currency"].id
                ).price
                order = form.save(commit=False)
                order.amount = int(
                    form.cleaned_data["crypto_amount"] * unit_price * 100
                )
                if order.amount <= 0:
                    raise Exception("the price should be more than 0")
                order.currency = "usd"
                order.user = request.user
                order.email = form.cleaned_data["email"]
                # Create a PaymentIntent with the order amount and currency
                intent = stripe.PaymentIntent.create(
                    amount=order.amount,
                    currency="usd",
                    automatic_payment_methods={
                        "enabled": True,
                    },
                )
                order.clientSecret = intent["client_secret"]
                order.save()
                return render(
                    request,
                    "coinmarketapp/checkout.html",
                    {
                        "clientSecret": intent["client_secret"],
                        "url": "http://"
                               + request.get_host()
                               + "/pay-result?order_id="
                               + str(order.id),
                        "email": order.email,
                        "amount": str(order.amount / 100),
                    },
                )
            except Exception as e:
                print(e)
                return HttpResponse("fail to create order")
    form = OrderForm()
    form.set(email=request.user.email)
    crypto_type = request.GET.get('crypto', '-1')
    try:
        if crypto_type != '-1':
            crypto_type = int(crypto_type)
            form.set(currency=CryptoCurrency.objects.get(id=crypto_type))
    except Exception as e:
        print(e)
    return render(request, "coinmarketapp/create_order.html", {"form": form})


@login_required
def render_sell_page(request, wallet_id):
    wallet = get_object_or_404(UserWallet, pk=wallet_id)
    if request.method == "POST":
        form = SellForm(request.POST)
        print(form.errors)
        if form.is_valid():
            unit_price = CryptoCurrency.objects.get(id=wallet.currency.id).price
            order = Order()
            order.amount = int(form.cleaned_data["crypto_amount"] * unit_price * 100)
            if order.amount <= 0:
                raise Exception("the price should be more than 0")
            order.currency = "usd"
            order.user = request.user
            order.email = form.cleaned_data["email"]
            order.crypto_currency = wallet.currency
            order.crypto_amount = form.cleaned_data["crypto_amount"]
            order.card_number = form.cleaned_data["card_number"]
            order.order_status = Order.SOLD
            wallet.amount -= form.cleaned_data["crypto_amount"]
            if wallet.amount < 0:
                raise ValidationError("You don't have enough currency to sell")
            with transaction.atomic():
                order.save()
                if wallet.amount == 0:
                    wallet.delete()
                else:
                    wallet.save()
            return render(request, "coinmarketapp/sell_result.html",
                          {"name": wallet.currency.name, "amount": order.crypto_amount,
                           "card": form.cleaned_data["card_number"], "money": str(order.amount / 100) + order.currency})
    if request.user.id != wallet.user.id:  # check if the wallet belongs to the user
        return render(request, "coinmarketapp/error.html")
    form = SellForm()
    form.set(email=request.user.email,
             currency=wallet.currency.name,
             wallet_id=wallet_id,
             price=wallet.currency.price,
             max_amount=wallet.amount)
    return render(request, "coinmarketapp/sell_currency.html", {"form": form})


@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(
        request,
        "coinmarketapp/checkout.html",
        {
            "clientSecret": order.clientSecret,
            "url": "http://"
                   + request.get_host()
                   + "/pay-result?order_id="
                   + str(order.id),
            "email": order.email,
            "amount": str(order.amount / 100),
        },
    )


@login_required
def pay_reslut(request):
    is_success = request.GET.get("redirect_status")
    if is_success == "succeeded":
        try:
            order = Order.objects.get(id=request.GET.get("order_id"))
            order.payment_intent = request.GET.get("payment_intent")
            order.payment_intent_client_secret = request.GET.get(
                "payment_intent_client_secret"
            )
            if order.order_status == Order.CREATED:  # only update the order status when it is created
                order.order_status = Order.COMPLETED
                with transaction.atomic():
                    order.save()
                    cur = UserWallet.objects.filter(currency=order.crypto_currency)
                    if cur.exists():
                        cur = cur[0]
                        cur.amount += order.crypto_amount
                        cur.save()
                    else:
                        UserWallet.objects.create(
                            user=request.user,
                            currency=order.crypto_currency,
                            amount=order.crypto_amount,
                        )
        except Exception as e:
            print(e)
            return render(request, "coinmarketapp/return.html")
    else:
        print("PaymentIntent faild: {}".format(is_success))
    return render(request, "coinmarketapp/return.html")


@login_required
def user_profile(request):
    # wallet = UserWallet.objects.filter(user=request.user)
    # result = {}
    # for w in wallet:
    #     key = w.currency.name
    #     result[key] = w.amount
    orders = Order.objects.filter(user=request.user).order_by('-created')
    for order in orders:
        order.amount = order.amount / 100
    return render(
        request,
        "coinmarketapp/user_profile.html",
        {
            "profile": UserProfile.objects.get(user=request.user),
            "wallets": UserWallet.objects.filter(user=request.user),
            "orders": orders,
        }
    )


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


def change_profile_picture(request):
    if request.method == 'POST':
        form = ChangeProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            profile.profile_picture = form.cleaned_data['new_profile_picture']
            profile.save()
            return redirect('user_profile')
    else:
        form = ChangeProfilePictureForm()

    return render(request, 'coinmarketapp/user_profile.html', {
        "profile": UserProfile.objects.get(user=request.user),
        "wallets": UserWallet.objects.filter(user=request.user),
        "orders": Order.objects.filter(user=request.user),
        'form': form
    })
