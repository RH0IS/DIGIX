# coinmarketapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('demo', views.demo, name='demo'),
    path('home/', views.crypto_list, name='crypto_list'),
    path('trends/', views.trends_view, name='trends_view'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('error', views.error, name='error'),
    # path('create_order', views.render_payment_page, name='create_order'),
    path('checkout', views.render_payment_page, name='render_payment_page'),
    # path('create-payment-intent', views.create_order, name='create-payment-intent'),
    path('pay-result', views.pay_reslut, name='pay-result'),
]
