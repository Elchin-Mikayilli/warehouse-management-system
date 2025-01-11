





# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouse/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouse/edit/<int:pk>/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouse/delete/<int:pk>/', views.warehouse_delete, name='warehouse_delete'),  # Delete URL
    path('warehouse/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('product/low-stock/', views.product_stock_warning, name='product_stock_warning'),
    path('product/create/<int:pk>/', views.product_create, name='product_create'),
]

