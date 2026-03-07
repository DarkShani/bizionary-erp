from rest_framework import serializers
from .models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        if not validated_data.get('total_cost'):
            quantity = validated_data.get('quantity_purchased', 0)
            unit_cost = validated_data.get('unit_cost', 0)
            validated_data['total_cost'] = quantity * unit_cost
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'total_cost' not in validated_data:
            quantity = validated_data.get('quantity_purchased', instance.quantity_purchased)
            unit_cost = validated_data.get('unit_cost', instance.unit_cost)
            validated_data['total_cost'] = quantity * unit_cost
        return super().update(instance, validated_data)
