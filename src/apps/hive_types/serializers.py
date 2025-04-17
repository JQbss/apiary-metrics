from rest_framework import serializers

from apps.hive_types.models import HiveType


class HiveTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = HiveType
        fields = '__all__'
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value