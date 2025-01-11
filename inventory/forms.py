


from django import forms
from .models import Warehouse, Product

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        exclude = ['created_at']
    
    # Handle the choices manually for 'status' and 'warehouse_type'
    status = forms.ChoiceField(choices=Warehouse._meta.get_field('status').choices)
    warehouse_type = forms.ChoiceField(choices=Warehouse._meta.get_field('warehouse_type').choices)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_at']
