# userauth/views.py
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, UserProfileForm
from django.shortcuts import render, redirect

# from coinmarketapp.models import UserWallet
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required





def signup(request):
    if request.method == 'POST':
        print(f"Received a POST request to the 'signup' view")

        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            print(user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        profile_form = UserProfileForm()
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
            return redirect('crypto_list')
        else:
            error_message = "Invalid username or password. Please try again!"
            messages.error(request, error_message)
            return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')

def custom_logout(request):
        logout(request)
        return redirect('login')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/change_password.html', {'form': form})
  