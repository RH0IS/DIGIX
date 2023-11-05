# coinmarketapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.crypto_list, name='crypto_list'),
    path('trends/', views.trends_view, name='trends_view'),
]
