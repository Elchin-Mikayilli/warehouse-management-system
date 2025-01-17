from django import forms
from .models import Warehouse, Product


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location', 'status', 'warehouse_type']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'warehouse_type': forms.Select(attrs={'class': 'form-control'}),
        }

    # Custom validation to ensure unique warehouse name per user
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure the warehouse has an associated user
        user = self.instance.user if self.instance.user else None
        
        if not user:
            raise forms.ValidationError("This warehouse must be associated with a user.")

        # Check if warehouse with the same name already exists for the same user
        if Warehouse.objects.filter(user=user, name__iexact=name).exclude(warehouse_code=self.instance.warehouse_code).exists():
            raise forms.ValidationError("A warehouse with this name already exists for this user.")
        
        return name

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve user from kwargs
        super().__init__(*args, **kwargs)
        
        if user:
            self.instance.user = user  # Set the user for this warehouse instance if provided

    # Custom validation to prevent deleting warehouse if it contains products
    def clean(self):
        cleaned_data = super().clean()
        warehouse = self.instance

        if warehouse.pk:  # Only check if the warehouse exists in the database
            if warehouse.products.exists():  # Use 'products' instead of 'product_set'
                raise forms.ValidationError("Cannot delete this warehouse because it contains products.")
        
        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'stock_quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_stock_quantity(self):
        stock_quantity = self.cleaned_data.get('stock_quantity')
        if stock_quantity is not None and stock_quantity < 1:
            raise forms.ValidationError('Please specify a valid stock quantity.')
        return stock_quantity


# ✅ EditNameForm (For Editing Product Name)
class EditNameForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ✅ EditPriceForm (For Editing Product Price)
class EditPriceForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ✅ DeleteProductForm (For Deleting a Product)
class DeleteProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = []  # No fields needed, deletion is handled separately

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['confirm_delete'] = forms.BooleanField(
            required=True, label="Are you sure you want to delete this product?", 
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )


# ✅ StockForm (For Managing Stock Quantity Actions in warehouse_detail)
class StockForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    action = forms.ChoiceField(
        choices=[('add', 'Add Stock')],  # Removed remove action
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Product
        fields = ['stock_quantity']
        widgets = {
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        quantity = cleaned_data.get('quantity')

        if action == 'add' and not quantity:
            raise forms.ValidationError('Quantity is required for add action.')

        return cleaned_data
