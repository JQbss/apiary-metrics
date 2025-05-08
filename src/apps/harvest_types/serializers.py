from rest_framework import serializers

from apps.harvest_types.models import HarvestType


class HarvestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestType
        fields = '__all__'
        read_only_fields = ['id']
