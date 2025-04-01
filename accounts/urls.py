from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('delivery/dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('update-order-status/<int:order_id>/<str:status>/', views.update_order_status, name='update_order_status'),    
]
