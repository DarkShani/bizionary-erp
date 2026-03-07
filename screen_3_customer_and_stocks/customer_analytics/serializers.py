from rest_framework import serializers
from .models import (
    Customer, CustomerBehavior, PurchaseRecord, 
    RecentActivity, CustomerInsight, CustomerKPI
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'full_name', 'email', 'phone', 'loyalty_tier', 'is_vip',
            'lifetime_value', 'total_purchases', 'average_order_value',
            'last_purchase_date', 'registration_date', 'churn_risk_score',
            'is_at_risk', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for quick customer entry"""
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone']


class CustomerBehaviorSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = CustomerBehavior
        fields = [
            'id', 'customer', 'customer_name', 'month', 'purchase_frequency',
            'total_spent', 'average_days_between_purchases', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PurchaseRecordSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = PurchaseRecord
        fields = [
            'id', 'customer', 'customer_name', 'purchase_date', 'amount',
            'items_count', 'payment_method', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RecentActivitySerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = RecentActivity
        fields = [
            'id', 'customer', 'customer_name', 'activity_type', 
            'description', 'metadata', 'timestamp', 'time_ago'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_time_ago(self, obj):
        from django.utils.timezone import now
        delta = now() - obj.timestamp
        
        if delta.days > 0:
            return f"{delta.days}d ago"
        elif delta.seconds >= 3600:
            return f"{delta.seconds // 3600}h ago"
        elif delta.seconds >= 60:
            return f"{delta.seconds // 60}m ago"
        else:
            return "Just now"


class CustomerInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInsight
        fields = [
            'id', 'insight_type', 'title', 'description', 'priority',
            'metric_value', 'recommendation', 'action_plan', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerKPISerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerKPI
        fields = [
            'id', 'date', 'total_customers', 'total_customers_change',
            'retention_rate', 'retention_rate_change', 'avg_lifetime_value',
            'avg_lifetime_value_change', 'churn_risk_percentage', 
            'churn_risk_change', 'vip_tier_count', 'regular_tier_count',
            'new_signup_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DashboardKPISerializer(serializers.Serializer):
    """Serializer for dashboard KPI overview"""
    total_customers = serializers.IntegerField()
    total_customers_change = serializers.DecimalField(max_digits=5, decimal_places=2)
    retention_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    retention_rate_change = serializers.DecimalField(max_digits=5, decimal_places=2)
    avg_lifetime_value = serializers.DecimalField(max_digits=12, decimal_places=2)
    avg_lifetime_value_change = serializers.DecimalField(max_digits=5, decimal_places=2)
    churn_risk_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    churn_risk_change = serializers.DecimalField(max_digits=5, decimal_places=2)


class LoyaltyDistributionSerializer(serializers.Serializer):
    """Serializer for loyalty tier distribution"""
    tier = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class BehaviorFrequencySerializer(serializers.Serializer):
    """Serializer for customer behavior frequency chart"""
    month = serializers.CharField()
    frequency_index = serializers.IntegerField()
