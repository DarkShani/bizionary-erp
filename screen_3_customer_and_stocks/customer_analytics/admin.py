from django.contrib import admin
from .models import (
    Customer, CustomerBehavior, PurchaseRecord, 
    RecentActivity, CustomerInsight, CustomerKPI
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'loyalty_tier', 'lifetime_value', 'total_purchases', 'is_at_risk', 'created_at']
    list_filter = ['loyalty_tier', 'is_vip', 'is_at_risk', 'is_active']
    search_fields = ['full_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(CustomerBehavior)
class CustomerBehaviorAdmin(admin.ModelAdmin):
    list_display = ['customer', 'month', 'purchase_frequency', 'total_spent']
    list_filter = ['month']
    search_fields = ['customer__full_name', 'customer__email']


@admin.register(PurchaseRecord)
class PurchaseRecordAdmin(admin.ModelAdmin):
    list_display = ['customer', 'purchase_date', 'amount', 'items_count', 'payment_method']
    list_filter = ['purchase_date', 'payment_method']
    search_fields = ['customer__full_name', 'customer__email']
    date_hierarchy = 'purchase_date'


@admin.register(RecentActivity)
class RecentActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'description', 'customer', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['description', 'customer__full_name']
    date_hierarchy = 'timestamp'


@admin.register(CustomerInsight)
class CustomerInsightAdmin(admin.ModelAdmin):
    list_display = ['insight_type', 'title', 'priority', 'metric_value', 'is_active', 'created_at']
    list_filter = ['insight_type', 'priority', 'is_active']
    search_fields = ['title', 'description']


@admin.register(CustomerKPI)
class CustomerKPIAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_customers', 'retention_rate', 'avg_lifetime_value', 'churn_risk_percentage']
    list_filter = ['date']
    date_hierarchy = 'date'
