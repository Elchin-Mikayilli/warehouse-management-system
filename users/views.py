# # users/views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import RegistrationForm, LoginForm

# # User Login View
# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('warehouse_list')  # Redirect to warehouse list after login
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

# # User Logout View
# def user_logout(request):
#     logout(request)
#     return redirect('login')  # Redirect to login page after logout

# # User Registration View
# def user_register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')  # Redirect to login after successful registration
#     else:
#         form = RegistrationForm()
#     return render(request, 'users/register.html', {'form': form})

# # Home View (Updated)
# def home(request):
#     return render(request, 'home.html')  # Render the home page template


# users/views.py
# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .forms import RegistrationForm

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('warehouse_list')  # Redirect to warehouse list after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# Home View
def home(request):
    return render(request, 'home.html')  # Render the home page template
