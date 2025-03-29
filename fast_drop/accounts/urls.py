from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('customer/', views.customer_home, name='customer_home'),
    path('delivery/', views.delivery_home, name='delivery_home'),
]
