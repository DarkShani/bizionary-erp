"""
ERP System Main URL Configuration
==================================

Root URL patterns for the entire application
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Dashboard API endpoints
    path('api/dashboard/', include('dashboard.urls')),
    
    # Screen 2: Sales & Items Management APIs
    path('api/screen2/', include('screen_2_sales_items.urls')),
    
    # Screen 4: Accounts & Finance APIs
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
]
