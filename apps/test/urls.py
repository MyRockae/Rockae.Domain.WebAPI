# urls.py
from django.urls import path
from .views import debug_credentials

urlpatterns = [
    path('debug-creds/', debug_credentials),
]