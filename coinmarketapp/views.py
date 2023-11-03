# coinmarketapp/views.py

from django.shortcuts import render
from .models import CryptoCurrency
import requests

def crypto_list(request):
    cryptocurrencies = CryptoCurrency.objects.all()
    data = {}
    # data["crypto_data"] = get_crypto_data()
    data = get_crypto_data()
    return render(request, 'coinmarketapp/crypto_list.html', {'cryptocurrencies': cryptocurrencies,'crypto_rates':data})

def index(request):
    data = {}
    data["crypto_data"] = get_crypto_data()
    return render(request, "myappF23/index.html", context=data)


# return the data received from api as json object
def get_crypto_data():
    # api_url = "https://api.coinmarketcap.com/v1/ticker/?limit=10"
    api_url = "http://api.coinlayer.com/live?access_key=cc193be204150f270335cb8652f14683"
    try:
        data = requests.get(api_url).json()

    except Exception as e:
        print(e)
        data = dict()
    rates = data['rates']
    return rates