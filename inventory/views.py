from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Warehouse, Product
from .forms import WarehouseForm, ProductForm

# View to list all warehouses with search functionality and pagination
@login_required
def warehouse_list(request):
    # Fix the indentation for the following line
    warehouses = Warehouse.objects.filter(user=request.user).order_by('-created_at')

    # Get the search query (if provided)
    search_query = request.GET.get('search', '')

    if search_query:
        warehouses = warehouses.filter(name__icontains=search_query)

    # Pagination logic
    paginator = Paginator(warehouses, 10)  # Show 10 warehouses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventory/warehouse_list.html', {
        'warehouses': page_obj,
        'search_query': search_query,
    })


# View to create a new warehouse
@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST, user=request.user)  # Pass user to the form
        if form.is_valid():
            warehouse = form.save(commit=False)
            warehouse.user = request.user  # Ensure the warehouse is linked to the logged-in user
            warehouse.save()
            messages.success(request, f'You have successfully created the warehouse: {warehouse.name}')
            return redirect('warehouse_list') # Redirect to product creation page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WarehouseForm()

    return render(request, 'inventory/warehouse_create.html', {
        'form': form
    })

# View to edit an existing warehouse
@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.name = request.POST.get('name')
        warehouse.location = request.POST.get('location')
        warehouse.status = request.POST.get('status')
        warehouse.save()
        return redirect('warehouse_list')

    return render(request, 'inventory/warehouse_edit.html', {'warehouse': warehouse})



# View to delete a warehouse
@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, warehouse_code=pk, user=request.user)

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
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)  # Use pk as the identifier

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.warehouse = warehouse  # Associate product with warehouse
            product.save()
            messages.success(request, f'Product {product.name} created successfully.')
            return redirect('warehouse_detail', pk=warehouse.pk)  # Redirect with pk
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, 'inventory/product_create.html', {
        'warehouse': warehouse,
        'form': form
    })


# View to display a warning for low stock products
@login_required
def product_stock_warning(request):
    products = Product.objects.filter(warehouse__user=request.user)
    low_stock_warning = [product for product in products if product.stock_quantity <= 10]

    return render(request, 'inventory/product_stock_warning.html', {
        'low_stock_warning': low_stock_warning
    })

# View to display the details of a specific warehouse
@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(Warehouse, warehouse_code=pk, user=request.user)  # Use warehouse_code
    products = Product.objects.filter(warehouse=warehouse)

    return render(request, 'inventory/warehouse_detail.html', {
        'warehouse': warehouse,
        'products': products
    })
