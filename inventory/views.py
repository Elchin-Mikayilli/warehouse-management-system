from uuid import UUID
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Warehouse, Product, Stock
from .forms import WarehouseForm, ProductForm, StockForm

# View to list all warehouses with search functionality and pagination
@login_required
def warehouse_list(request):
    # Filter warehouses by the logged-in user
    warehouses = Warehouse.objects.filter(user=request.user).order_by('-created_at')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        warehouses = warehouses.filter(name__icontains=search_query)

    # Pagination setup
    paginator = Paginator(warehouses, 10)  # 10 warehouses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/warehouse_list.html', {
        'warehouses': page_obj,
        'search_query': search_query,
    })

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST, user=request.user)  # Pass the user to the form
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.user = request.user  # Ensure the user is associated with the warehouse
            warehouse.save()
            messages.success(request, f'You have successfully created the warehouse: {warehouse.name}')
            return redirect('warehouse_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WarehouseForm()

    return render(request, 'inventory/warehouse_create.html', {'form': form})

# View to edit an existing warehouse
@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)  # Ensure the warehouse belongs to the user
    if request.method == 'POST':
        warehouse.name = request.POST.get('name')
        warehouse.location = request.POST.get('location')
        warehouse.status = request.POST.get('status')
        warehouse.save()
        messages.success(request, f'Warehouse {warehouse.name} updated successfully.')
        return redirect('warehouse_list')

    return render(request, 'inventory/warehouse_edit.html', {'warehouse': warehouse})

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

# View to create a product and associate it with a warehouse
@login_required
def product_create(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.warehouse = warehouse
            product.user = request.user  # Assign user to product
            product.save()

            # Handle initial stock if provided
            initial_stock = int(request.POST.get('initial_stock', 0))
            if initial_stock > 0:
                Stock.objects.create(product=product, quantity_added=initial_stock)
                product.update_stock(initial_stock, 'add')

            messages.success(request, f'Product {product.name} created successfully.')
            return redirect('warehouse_detail', pk=warehouse.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, 'inventory/product_create.html', {
        'warehouse': warehouse,
        'form': form
    })

# View to edit an existing product
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, warehouse__user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {product.name} updated successfully.')
            return redirect('warehouse_detail', pk=product.warehouse.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/product_edit.html', {'form': form, 'product': product})

# View to delete a product
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, warehouse__user=request.user)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product {product.name} has been deleted successfully.')
        return redirect('warehouse_detail', pk=product.warehouse.pk)

    return render(request, 'inventory/product_delete.html', {
        'product': product
    })

# View to manage stock actions (add stock)
@login_required
def add_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = StockForm(request.POST, instance=product)
        if form.is_valid():
            action = form.cleaned_data['action']
            quantity = form.cleaned_data['quantity']

            if action == 'add':
                product.stock_quantity += quantity
            # Remove action has been removed

            product.save()
            return redirect('product_stock_warning')

    else:
        form = StockForm(instance=product)

    return render(request, 'product/add_stock.html', {'form': form, 'product': product})

# View to display warehouse details, products, and stock management
@login_required
def warehouse_detail(request, pk):
    # Fetch the warehouse object
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)
    
    # Fetch products related to this warehouse
    products = Product.objects.filter(warehouse=warehouse).order_by('-created_at')

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data.get('action')
            product_id = request.POST.get('product_id')  # This is the product id (UUID)
            quantity = form.cleaned_data.get('quantity')

            try:
                # Ensure the product_id is correctly converted to a UUID object
                if isinstance(product_id, str):  # Ensure product_id is a string
                    product_id = UUID(product_id)
                else:
                    raise ValueError("Invalid product ID format")
            except (ValueError, TypeError) as e:
                # If there's an issue converting, add a message
                messages.error(request, f'Invalid product ID: {e}')
                return redirect('warehouse_detail', pk=warehouse.pk)

            # Fetch the product object using UUID
            product = get_object_or_404(Product, id=product_id, warehouse=warehouse)

            if action == 'add':
                # Add stock to product
                product.stock_quantity += quantity
                product.save()
                Stock.objects.create(product=product, quantity_added=quantity)
                messages.success(request, f'Added {quantity} units to {product.name}.')
            elif action == 'delete':
                # Delete product from warehouse
                product.delete()
                messages.success(request, f'Product {product.name} deleted successfully.')

            return redirect('warehouse_detail', pk=warehouse.pk)
    else:
        form = StockForm()

    return render(request, 'inventory/warehouse_detail.html', {
        'warehouse': warehouse,
        'products': products,
        'form': form
    })

# View to show products with low stock
@login_required
def product_stock_warning(request):
    stock_threshold = 10
    low_stock_products = Product.objects.filter(stock_quantity__lt=stock_threshold)

    return render(request, 'inventory/product_stock_warning.html', {
        'low_stock_products': low_stock_products,
        'stock_threshold': stock_threshold,
    })
