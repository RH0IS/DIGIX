# coinmarketapp/views.py
import json
import requests
import stripe
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .models import CryptoCurrency, UserWallet, Order, trending_crypto
from .forms import RowSelectionForm, OrderForm

stripe.api_key = "sk_test_51O4pjuHl9Bqmml9jt2gupSLgAY6JjnvhQ9YaHuNHWZJOZZVZdeZHD67aG6WOkxXxIyy7OBQQKNdrWH90U3qaAVhO00tHqCFiRH"


def ticker_base(request):
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

        # Pass the cryptocurrency data and additional data to the template
        return render(
            request,
            "coinmarketapp/base.html",
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

        # data = response.json()
        # Extract relevant data from the API response
        # CryptoCurrency.objects.all().delete()
        # cryptocurrencies = []
        # for crypto in data['data']:
        #     name = crypto['name']
        #     symbol = crypto['symbol']
        #     market_cap = crypto['quote']['USD']['market_cap']
        #     price = crypto['quote']['USD']['price']
        #     volume_24h = crypto['quote']['USD']['percent_change_1h']  # Verify the correct key
        #
        #     crypto_obj = CryptoCurrency(
        #         name=name,
        #         symbol=symbol,
        #         market_cap=market_cap,
        #         price=price,
        #         volume_24h=volume_24h
        #     )
        #     crypto_obj.save()
        #     cryptocurrencies = CryptoCurrency.objects.all()

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
    symbol=crypto_by_name.symbol
    cookie = request.COOKIES.get(symbol)
    #print(symbol)
    clist=top_crypto_list(request)
    trending_currencies=trending_crypto.objects.all()
    tlist=trending_currencies[:4]
    total_cryptos = len(trending_currencies)
    highest_ranked_crypto = max(trending_currencies, key=lambda x: x.rank)
    lowest_ranked_crypto = min(trending_currencies, key=lambda x: x.rank)
    response = render(request, 'coinmarketapp/crypto_page.html', {
        "cpt": crypto_by_name,
        "clist":clist,
        "trending_currencies": tlist,
        "total_cryptos": total_cryptos,
        "highest_ranked_crypto": highest_ranked_crypto,
        "lowest_ranked_crypto": lowest_ranked_crypto,
    })
    if not cookie:
        response.set_cookie(symbol,'1')
    else:
        cookie=int(cookie)+1
        response.set_cookie(symbol,cookie)
    #print(clist)
    return response



@api_view(["GET"])
@throttle_classes([UserRateThrottle])
def demo(request):
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
        # Parse the JSON response
        __update_crypto_currency(response.json())
        data = response.json()
        # Extract relevant data from the API response
        CryptoCurrency.objects.all().delete()

        for crypto in data["data"]:
            name = crypto["name"]
            symbol = crypto["symbol"]
            market_cap = crypto["quote"]["USD"]["market_cap"]
            price = crypto["quote"]["USD"]["price"]
            volume_24h = crypto["quote"]["USD"]["percent_change_1h"]

            crypto_obj = CryptoCurrency(
                name=name,
                symbol=symbol,
                market_cap=market_cap,
                price=price,
                volume_24h=volume_24h,
            )
            crypto_obj.save()

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
                unit_price = CryptoCurrency.objects.get(
                    id=form.cleaned_data["crypto_currency"].id
                ).price
                order = form.save(commit=False)
                order.amount = int(
                    form.cleaned_data["crypto_amount"] * unit_price * 100
                )
                if order.amount <= 0:
                    raise Exception("the price should be more than 0")
                order.currency = "cad"
                order.user = request.user
                order.email = form.cleaned_data["email"]
                order.save()
                # Create a PaymentIntent with the order amount and currency
                intent = stripe.PaymentIntent.create(
                    amount=order.amount,
                    currency="cad",
                    automatic_payment_methods={
                        "enabled": True,
                    },
                )
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
                    },
                )
            except Exception as e:
                messages.error(request, e)
                return HttpResponse("fail to create order")
    form = OrderForm()
    form.set(email=request.user.email)
    return render(request, "coinmarketapp/create_order.html", {"form": form})


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
            if (
                order.order_status == Order.CREATED
            ):  # only update the order status when it is created
                order.order_status = Order.COMPLETED
                with transaction.atomic():
                    order.save()
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
    return render(
        request,
        "coinmarketapp/user_profile.html",
        {
            "wallets": UserWallet.objects.filter(user=request.user),
            "orders": Order.objects.filter(user=request.user),
        },
    )
