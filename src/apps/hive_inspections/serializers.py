from rest_framework import serializers

from apps.hive_inspections.models import HiveInspection
from apps.hives.models import Hive


class HiveInspectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = HiveInspection
        fields = '__all__'
        read_only_fields = ['id']

    def validate_hive(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Authentication required.")


        try:
            hive = Hive.objects.get(id=value.id)
        except Hive.DoesNotExist:
            raise serializers.ValidationError("Hive does not exist.")

        if request and hasattr(request, 'user'):
            user = request.user
            if not user.apiarymembership_set.filter(
                    apiary_id=hive.apiary.id,
                    role__in=['OWNER', 'EDITOR']
            ).exists():
                raise serializers.ValidationError(
                    "You do not have permission to create a hive inspection for this hive.")
        return value
