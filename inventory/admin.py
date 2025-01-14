

from django.contrib import admin
from .models import Warehouse, Product, Stock

# Warehouse model registration with enhancements
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'location', 'status', 'warehouse_type', 'created_at', 'warehouse_code')
    search_fields = ('name', 'location', 'warehouse_code')
    list_filter = ('status', 'warehouse_type')  # Allows filtering by status and warehouse type
    list_display_links = ('name',)  # Make warehouse name clickable for easy navigation
    ordering = ('created_at',)  # Optionally order warehouses by their creation date

# Product model registration with improvements
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'warehouse', 'price', 'stock_quantity', 'created_at')  # Display relevant fields
    list_filter = ('warehouse',)  # Filter products by warehouse
    search_fields = ('name',)  # Allow searching by product name
    ordering = ('created_at',)  # Optionally order products by their creation date

# Stock model registration with enhancements
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_added', 'quantity_removed', 'total_stock', 'date')  # Display stock details
    list_filter = ('product',)  # Filter stock entries by product
    search_fields = ('product__name',)  # Search by product name
    ordering = ('-date',)  # Order by most recent stock movements

    # Dynamic method to calculate total stock
    def total_stock(self, obj):
        return obj.quantity_added - obj.quantity_removed
    total_stock.admin_order_field = 'quantity_added'  # Make it sortable by 'quantity_added'
    total_stock.short_description = 'Total Stock'  # Provide a friendly name for the column

# Register models with the Django admin interface
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Stock, StockAdmin)
