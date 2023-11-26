# userauth/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),        
    path('change_password/', views.change_password, name='change_password'),
    path('user_profile/', views.user_profile, name='user_profile'),
]
