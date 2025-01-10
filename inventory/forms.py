# inventory/forms.py
from django import forms
from .models import Warehouse, Product

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['created_at']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_at']
