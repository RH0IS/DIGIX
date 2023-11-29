# coinmarketapp/urls.py

from django.urls import path
from . import views
from .views import get_exchange_rates

urlpatterns = [
    # path('home/', views.crypto_list, name='crypto_list'),
    path("", views.demo, name="demo"),
    path("demo", views.demo, name="demo"),
    path("home/", views.trends_view, name="crypto_list"),
    # path("home/", views.trends_view, name="trends_view"),
    path("trends/", views.trends_view, name="trends_view"),
    path("user_profile/", views.user_profile, name="user_profile"),
    path("error", views.error, name="error"),
    # path('create_order', views.render_payment_page, name='create_order'),
    path('checkout', views.render_payment_page, name='render_payment_page'),
    # path('create-payment-intent', views.create_order, name='create-payment-intent'),
    path('complete_order/<int:order_id>', views.complete_order, name='complete_order'),
    path('pay-result', views.pay_reslut, name='pay-result'),
    path('currencies/<str:currname>/', views.cypto_by_name, name='cypto_by_name'),
    path('exchange', views.exchange, name='exchange'),
    path('change_profile_picture', views.change_profile_picture, name='change_profile_picture'),
    path('get_exchange_rate/<str:from_currency>/<str:to_currency>/', views.get_exchange_rate, name='get_exchange_rate'),
    path('sell_curriency/<int:wallet_id>', views.render_sell_page, name='sell_curriency'),
]
