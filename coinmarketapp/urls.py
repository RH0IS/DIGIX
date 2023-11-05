# coinmarketapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='crypto_list'),
    path('home',views.crypto_list, name='crypto_list' ),
    path('error',views.error, name='error' ),
]
