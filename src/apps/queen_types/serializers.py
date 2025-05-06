from rest_framework import serializers

from apps.queen_types.models import QueenType


class QueenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueenType
        fields = '__all__'
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value
