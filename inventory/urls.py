




# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouses/edit/<int:pk>/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouses/delete/<int:pk>/', views.warehouse_delete, name='warehouse_delete'),
]
