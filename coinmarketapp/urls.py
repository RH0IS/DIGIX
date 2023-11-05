# coinmarketapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.demo, name='demo'),
    path('demo', views.demo, name='demo'),
    path('home/',views.crypto_list, name='crypto_list' ),
    path('trends/', views.trends_view, name='trends_view'),
    path('error',views.error, name='error' ),
]
