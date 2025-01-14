

from django.urls import path
from . import views

urlpatterns = [
    path('warehouse/', views.warehouse_list, name='warehouse_list'),
    path('warehouse/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouse/edit/<uuid:pk>/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouse/delete/<uuid:pk>/', views.warehouse_delete, name='warehouse_delete'),
    path('warehouse/detail/<uuid:pk>/', views.warehouse_detail, name='warehouse_detail'),

    # Product views
    path('product/create/<uuid:pk>/', views.product_create, name='product_create'),
    path('product/stock-warning/', views.product_stock_warning, name='product_stock_warning'),
]
