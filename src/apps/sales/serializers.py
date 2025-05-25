from rest_framework import serializers

from apps.sales.models import Sale
from django.utils import timezone


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'date', 'quantity', 'prize', 'unit', 'type', 'created_at', 'updated_at']
        read_only_fields = ['id']

    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_prize(self, value):
        if value <= 0:
            raise serializers.ValidationError("Prize must be greater than zero.")
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
