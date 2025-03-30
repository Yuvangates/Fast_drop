from django.urls import path
from . import views

app_name='stores'

urlpatterns = [
    path('',views.stores_list,name='list'),
    # path('create',views.store_create,name='create'),
    # path('<slug:slug>/', views.store_details, name='detail'), 
     path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/add-item/', views.add_item, name='add_item'),
     path('items/', views.items_list, name='items_list'), 
]

