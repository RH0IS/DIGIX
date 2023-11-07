# userauth/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
        path('login/', views.login_view, name='login'),

    path('user_profile/', views.user_profile, name='user_profile'),
]
