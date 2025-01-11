

#inventory.models
from django.db import models
from django.contrib.auth.models import User

# Warehouse model (depends on Users)
class Warehouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('maintenance', 'Under Maintenance'),
            ('closed', 'Closed')
        ],
        default='active'
    )
    warehouse_type = models.CharField(
        max_length=50,
        choices=[
            ('regular', 'Regular'),
            ('refrigerated', 'Refrigerated'),
            ('storage', 'Storage Only')
        ],
        default='regular'
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Owned by {self.user.username})"

    # No need for the custom methods for `get_status_display` and `get_warehouse_type_display`
    # Django already handles this for you automatically.

# Product model (depends on Warehouse)
class Product(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()  # Initial stock quantity
    stock_threshold = models.PositiveIntegerField(default=20)  # Low stock threshold
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def check_stock_warning(self):
        """
        Checks if the product stock is below the threshold and returns a warning message if true.
        """
        total_stock = sum(stock.quantity_added - stock.quantity_removed for stock in self.stock_movements.all())
        if total_stock < self.stock_threshold:
            return f"Warning: {self.name} stock is low. Only {total_stock} units left."
        return None


# Stock model (depends on Product)
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity_added = models.PositiveIntegerField(default=0)  # Quantity added to stock
    quantity_removed = models.PositiveIntegerField(default=0)  # Quantity removed from stock
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock movement for {self.product.name} on {self.date}"
