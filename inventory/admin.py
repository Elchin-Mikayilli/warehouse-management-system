# inventory/admin.py

from django.contrib import admin
from .models import Warehouse, Product, Stock

# Register Warehouse model
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'status', 'created_at')
    search_fields = ('name', 'location')

# Register Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'warehouse', 'price', 'stock_quantity', 'created_at')
    list_filter = ('warehouse',)  # Filter by warehouse in the admin interface
    search_fields = ('name',)

# Register Stock model
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_added', 'quantity_removed', 'date')
    list_filter = ('product',)  # Filter by product in the admin interface
    search_fields = ('product__name',)

# Register all models
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
