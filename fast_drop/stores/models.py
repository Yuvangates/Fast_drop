from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    # latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    manager = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ✅ Correctly point to custom User model
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'manager'},  # Optional: restrict to managers only
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.store.name}"
