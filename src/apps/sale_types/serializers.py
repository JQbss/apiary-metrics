from rest_framework import serializers

from apps.sale_types.models import SaleType


class SaleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleType
        fields = '__all__'
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value