from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import User

def home(request):
    return redirect('accounts:login')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_based_on_role(user)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect_based_on_role(user)
            else:
                messages.error(request, "Invalid username or password!")  # Show error on invalid login
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def redirect_based_on_role(user):
    if user.role == 'customer':
        return redirect('accounts:customer_home')
    elif user.role == 'manager':
        return redirect('accounts:customer_home')  # Ensure this exists!
    elif user.role == 'delivery_agent':
        return redirect('accounts:delivery_home')
    return redirect('accounts:login')



@login_required
def customer_home(request):
    return render(request, 'accounts/customer_home.html')

@login_required
def delivery_home(request):
    return render(request, 'accounts/delivery_home.html')

def user_logout(request):
    logout(request)
    return redirect('login')
