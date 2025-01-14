

from django import forms
from .models import Warehouse, Product

# ✅ Warehouse Form
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'status', 'warehouse_type']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'warehouse_type': forms.Select(attrs={'class': 'form-control'})
        }

    # Custom validation for warehouse name to ensure uniqueness per user
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = self.instance.user  # Get the user from the instance (either new or editing)
        
        # Check if another warehouse with the same name exists for the same user
        if Warehouse.objects.filter(user=user, name__iexact=name).exclude(warehouse_code=self.instance.warehouse_code).exists():
            raise forms.ValidationError("A warehouse with this name already exists for this user.")
        return name

    # If you need to restrict warehouses based on the logged-in user
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from the view or context
        super(WarehouseForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user  # Assign the logged-in user to the warehouse


# ✅ Product Form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock_quantity', 'price']  # Removed 'description' since it's not in the model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
