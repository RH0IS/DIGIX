# coinmarketapp/views.py

from django.shortcuts import render
from .models import CryptoCurrency

def crypto_list(request):
    cryptocurrencies = CryptoCurrency.objects.all()
    return render(request, 'coinmarketapp/crypto_list.html', {'cryptocurrencies': cryptocurrencies})
