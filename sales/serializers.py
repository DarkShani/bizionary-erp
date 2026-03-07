from rest_framework import serializers
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        if not validated_data.get('total_price'):
            quantity = validated_data.get('quantity_sold', 0)
            unit_price = validated_data.get('unit_price', 0)
            validated_data['total_price'] = quantity * unit_price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'total_price' not in validated_data:
            quantity = validated_data.get('quantity_sold', instance.quantity_sold)
            unit_price = validated_data.get('unit_price', instance.unit_price)
            validated_data['total_price'] = quantity * unit_price
        return super().update(instance, validated_data)
