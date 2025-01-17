import uuid
from django.db import models
from django.contrib.auth.models import User


# ✅ Warehouse model
class Warehouse(models.Model):
    warehouse_code = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='warehouses'
    )
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('maintenance', 'Under Maintenance'),
            ('closed', 'Closed'),
        ],
        default='active'
    )
    warehouse_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('cold', 'Cold'),
        ],
        default='general'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Owned by {self.user.username}, Status: {self.get_status_display()})"

    # Method to check if the warehouse can be deleted
    def can_be_deleted(self):
        return not self.products.exists()  # Check if there are any related products

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


# ✅ Product model with UUID id field
class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=255)
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='products'  # Specify reverse relation for warehouse.products
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return f"{self.name} ({self.warehouse.name})"

    # Method to update stock
    def update_stock(self, quantity, action):
        """Update stock quantity based on action."""
        if action == 'add':
            self.stock_quantity += quantity
        elif action == 'remove' and self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
        else:
            raise ValueError("Invalid quantity or action.")
        self.save()

    class Meta:
        unique_together = ('name', 'warehouse')
        indexes = [
            models.Index(fields=['name', 'warehouse']),
        ]


# ✅ Stock model to track movements
class Stock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stocks'
    )
    quantity_added = models.PositiveIntegerField(default=0)
    quantity_removed = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stock movement for {self.product.name} on {self.date.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        """Override save to update stock quantity for the product."""
        if self.quantity_added > 0:
            self.product.update_stock(self.quantity_added, 'add')
        if self.quantity_removed > 0:
            self.product.update_stock(self.quantity_removed, 'remove')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stock Movements"
        ordering = ['-date']
