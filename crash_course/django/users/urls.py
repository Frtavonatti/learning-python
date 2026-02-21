from django.urls import path
# from django.contrib.auth.views import login  # Deprecated en Django 1.11, eliminado en Django 2.0+
from django.contrib.auth.views import LoginView

from . import views

app_name = "users"

urlpatterns = [
  # path("login/", login, {'template_name': 'users/login.html'}, name='login'),  # Legacy login view
  # path("login/", views.login_view, name='login'),  # Custom login view
  path("login/", LoginView.as_view(template_name='users/login.html'), name='login'),
  path("logout/", views.logout_view, name='logout'),
  path("register/", views.register, name='register'),
]