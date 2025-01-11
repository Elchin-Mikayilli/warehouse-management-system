

# # users/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('register/', views.user_register, name='register'),
# ]

# users/urls.py
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use built-in LogoutView
    path('register/', views.user_register, name='register'),
]
