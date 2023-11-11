# coinmarketapp/urls.py

from django.urls import path
from . import views

from django.conf.urls import include
from django.contrib import admin

urlpatterns = [
    path('', views.crypto_list, name='crypto_list'),
    path('trends/', views.trends_view, name='trends_view'),
<<<<<<< Updated upstream
=======
    path('error',views.error, name='error' ),
    path('orders',views.orders, name='orders')
    # url(r'^admin/', include(admin.site.urls)),

>>>>>>> Stashed changes
]
