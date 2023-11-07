# coinmarketapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('demo', views.demo, name='demo'),
    path('home/', views.crypto_list, name='crypto_list'),
    path('trends/', views.trends_view, name='trends_view'),
    path('error', views.error, name='error'),
    path('checkout', views.payment_test, name='payment_test_page'),
    path('create-payment-intent', views.create_payment, name='create-payment-intent'),
    path('payment-result', views.payment_result, name='payment-result'),
]
