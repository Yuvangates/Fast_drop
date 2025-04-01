from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from stores.models import CartItem
from django.db import transaction

@login_required
def order_list(request):
    """View to display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View to display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('stores:cart')
    
    total_amount = sum(item.subtotal for item in cart_items)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total_amount,
                    address=request.POST['address'],
                    city=request.POST['city'],
                    state=request.POST['state'],
                    pincode=request.POST['pincode'],
                    payment_method=request.POST['payment_method']
                )
                
                # Create order items and update stock
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        item=cart_item.item,
                        quantity=cart_item.quantity,
                        price=cart_item.item.price
                    )
                    # Update stock
                    cart_item.item.stock -= cart_item.quantity
                    cart_item.item.save()
                
                # Clear the cart
                cart_items.delete()
                
                messages.success(request, 'Order placed successfully!')
                return redirect('orders:order_detail', order_id=order.id)
                
        except Exception as e:
            messages.error(request, 'An error occurred while placing your order. Please try again.')
            return redirect('orders:create_order')
    
    return render(request, 'orders/order_form.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@csrf_exempt
@login_required
def update_order_status(request, order_id, status):
    try:
        order = Order.objects.get(id=order_id, delivery_agent=request.user)
        if status in ['PICKED', 'DELIVERED']:
            order.status = status
            order.save()
            return JsonResponse({'status': 'success', 'message': f'Order marked as {status}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid status provided'})
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Order not found'})