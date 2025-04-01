from django.db import models
from django.conf import settings
from stores.models import Item
from django.utils.timezone import now, timedelta
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PICKED', 'Picked'),  # New status for picked orders
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI'),
        ('CARD', 'Card Payment'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.BooleanField(default=False)
    
    # Delivery Address Fields
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Grouping Orders for Optimization
    group_id = models.UUIDField(default=uuid.uuid4, editable=False)
    delivery_agent_location = models.CharField(max_length=255, blank=True, null=True)  # Starting location for agent

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
    # Group orders placed within 4 minutes into the same group
        if not self.group_id:
            recent_order = Order.objects.filter(
                created_at__gte=now() - timedelta(minutes=4),
                status__in=['PENDING', 'CONFIRMED']
            ).order_by('-created_at').first()
            if recent_order:
                self.group_id = recent_order.group_id

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.item.name} x {self.quantity}'
