from rest_framework import serializers
from django.utils import timezone

from apps.hives.models import Hive
from apps.queens.models import Queen


class QueenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queen
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

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
                    "You do not have permission to create a queen for this hive.")
        return value

    def validate_date(self, value):
        if not value:
            raise serializers.ValidationError("Queen date cannot be empty.")
        elif value > timezone.now().date():
            raise serializers.ValidationError("Queen date cannot be in the future.")
        return value
