# coinmarketapp/urls.py

from django.urls import path
from . import views
from .views import get_exchange_rates

urlpatterns = [
    path('', views.demo, name='demo'),
    path('demo', views.demo, name='demo'),
    path('home/',views.crypto_list, name='crypto_list' ),
    path('trends/', views.trends_view, name='trends_view'),
    path('error',views.error, name='error' ),
    path('exchange', views.exchange, name='exchange'),
    path('get_exchange_rate/<str:from_currency>/<str:to_currency>/', views.get_exchange_rate, name='get_exchange_rate'),
]
