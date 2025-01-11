


from django.shortcuts import render, redirect, get_object_or_404
from .models import Warehouse, Product, Stock
from .forms import WarehouseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# View to list all warehouses with search functionality
@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    if search_query:
        warehouses = warehouses.filter(name__icontains=search_query)

    return render(request, 'inventory/warehouse_list.html', {
        'warehouses': warehouses,
        'search_query': search_query
    })

# View to create a new warehouse
@login_required
def warehouse_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')
        status = request.POST.get('status')
        warehouse_type = request.POST.get('warehouse_type')

        warehouse = Warehouse.objects.create(
            user=request.user,
            name=name,
            location=location,
            capacity=capacity,
            status=status,
            warehouse_type=warehouse_type
        )
        messages.success(request, f'You have successfully created the warehouse: {warehouse.name}')
        return redirect('warehouse_detail', pk=warehouse.pk)

    return render(request, 'inventory/warehouse_create.html')

# View to see the warehouse details along with products and stock management
@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)
    products = Product.objects.filter(warehouse=warehouse)

    low_stock_warning = [product for product in products if product.stock_quantity <= 10]

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        action = request.POST.get('action')

        if quantity:
            quantity = int(quantity)
        else:
            messages.error(request, "Quantity is required.")
            return redirect('warehouse_detail', pk=pk)

        product = get_object_or_404(Product, pk=product_id, warehouse=warehouse)

        if action == 'add':
            Stock.objects.create(product=product, quantity_added=quantity)
            product.stock_quantity += quantity
        elif action == 'remove':
            if product.stock_quantity >= quantity:
                Stock.objects.create(product=product, quantity_removed=quantity)
                product.stock_quantity -= quantity
            else:
                messages.error(request, f"Not enough stock to remove for {product.name}.")

        product.save()
        messages.success(request, f'Stock updated for {product.name}.')

    return render(request, 'inventory/warehouse_detail.html', {
        'warehouse': warehouse,
        'products': products,
        'low_stock_warning': low_stock_warning
    })

# View to edit an existing warehouse
@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, f'Warehouse {warehouse.name} updated successfully.')
            return redirect('warehouse_detail', pk=warehouse.pk)
    else:
        form = WarehouseForm(instance=warehouse)

    return render(request, 'inventory/warehouse_edit.html', {
        'form': form,
        'warehouse': warehouse
    })

# View to delete a warehouse
@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)

    if request.method == 'POST':
        warehouse.delete()
        messages.success(request, f'Warehouse {warehouse.name} has been deleted successfully.')
        return redirect('warehouse_list')

    return render(request, 'inventory/warehouse_delete.html', {
        'warehouse': warehouse
    })

# View to create a new product in a warehouse
@login_required
def product_create(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))
        stock_quantity = int(request.POST.get('stock_quantity'))

        if price < 0 or stock_quantity < 0:
            messages.error(request, "Price and stock quantity must be positive values.")
            return render(request, 'inventory/product_create.html', {'warehouse': warehouse})

        product = Product.objects.create(
            warehouse=warehouse,
            name=name,
            price=price,
            stock_quantity=stock_quantity
        )
        messages.success(request, f'Product {product.name} created successfully.')
        return redirect('warehouse_detail', pk=warehouse.pk)

    return render(request, 'inventory/product_create.html', {
        'warehouse': warehouse
    })

# View to display a warning for low stock products
@login_required
def product_stock_warning(request):
    products = Product.objects.filter(warehouse__user=request.user)
    low_stock_warning = [product for product in products if product.stock_quantity <= 10]

    return render(request, 'inventory/product_stock_warning.html', {
        'low_stock_warning': low_stock_warning
    })