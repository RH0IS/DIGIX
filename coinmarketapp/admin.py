# coinmarketapp/admin.py

from django.contrib import admin
from .models import CryptoCurrency

# @admin.register(CryptoCurrency)
# class CryptoCurrencyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'symbol', 'market_cap', 'price', 'volume_24h')
#     list_filter = ('name', 'symbol')
#     search_fields = ('name', 'symbol')

admin.site.register(CryptoCurrency)