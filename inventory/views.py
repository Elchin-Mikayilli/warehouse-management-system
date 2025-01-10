

# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Warehouse
from .forms import WarehouseForm
from django.contrib.auth.decorators import login_required

# View to list all warehouses
@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.filter(user=request.user)
    
    # Searching functionality
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
        form = WarehouseForm(request.POST)
        if form.is_valid():
            # Associate warehouse with the logged-in user
            warehouse = form.save(commit=False)
            warehouse.user = request.user
            warehouse.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm()
    
    return render(request, 'inventory/warehouse_create.html', {'form': form})

# View to edit a warehouse
@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            return redirect('warehouse_list')
    else:
        form = WarehouseForm(instance=warehouse)
    
    return render(request, 'inventory/warehouse_edit.html', {'form': form, 'warehouse': warehouse})

# View to delete a warehouse
@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk, user=request.user)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('warehouse_list')
    
    return render(request, 'inventory/warehouse_delete.html', {'warehouse': warehouse})
