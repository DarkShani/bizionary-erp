from django.contrib import admin
from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'supplier_name', 'quantity_purchased', 'total_cost', 'purchase_date', 'payment_status']
    list_filter = ['purchase_date', 'payment_status']
    search_fields = ['supplier_name', 'product__name']
    readonly_fields = ['created_at', 'updated_at', 'total_cost']
    date_hierarchy = 'purchase_date'
