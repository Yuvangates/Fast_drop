from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import User 
from stores.models import Store, Item
from django.shortcuts import get_object_or_404
from orders.models import Order
from django.http import JsonResponse
from utils.google_maps import get_optimized_route
from django.conf import settings

def home(request):
    """Home page view that's accessible to everyone"""
    return render(request, 'home.html')

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

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect_based_on_role(user)
                else:
                    messages.error(request, "Your account is inactive!")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Invalid form submission!")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def redirect_based_on_role(user):
    if user.role == 'customer':
        return redirect('accounts:customer_dashboard')
    elif user.role == 'manager':
        return redirect('accounts:manager_dashboard')
    elif user.role == 'delivery_agent':
        return redirect('accounts:delivery_dashboard')
    return redirect('accounts:login')

@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('accounts:login')
    return render(request, 'accounts/customer_dashboard.html')

@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('accounts:login')
    stores = Store.objects.filter(manager=request.user)
    items = Item.objects.filter(store__in=stores)
    context = {
        'stores': stores,
        'items': items,
    }
    return render(request, 'accounts/manager_dashboard.html', context)

@login_required
def delivery_dashboard(request):
    if request.user.role != 'delivery_agent':
        return redirect('accounts:login')
        
    # Get active deliveries for the delivery agent
    active_deliveries = Order.objects.filter(
        delivery_agent=request.user,
        status__in=['CONFIRMED', 'PICKED']
    ).order_by('created_at')

    # Get route data for the map
    polyline = None
    legs = None
    if active_deliveries.exists():
        polyline, legs = get_optimized_route(active_deliveries)

    context = {
        'active_deliveries': active_deliveries,
        'polyline': polyline,
        'legs': legs,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'accounts/delivery_dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('accounts:home')

@login_required
def update_order_status(request, order_id, status):
    """Update order status (PICKED/DELIVERED) and notify customer if needed."""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        
        if status in ['PICKED', 'DELIVERED']:
            order.status = status
            order.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid status!'}, status=400)

    return JsonResponse({'error': 'Invalid request!'}, status=405)
