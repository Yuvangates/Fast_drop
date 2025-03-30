from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('manager', 'Manager'),
        ('delivery_agent', 'Delivery Agent'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
