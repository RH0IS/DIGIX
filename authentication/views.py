# userauth/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import UserProfile

def signup(request):
    if request.method == 'POST':
        print(f"Received a POST request to the 'signup' view")

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            # login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.registered:
                return render(request, 'authentication/login.html')
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'authentication/registered_user.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_profile')
        else:
            error_message = "Invalid username or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'authentication/login.html')
