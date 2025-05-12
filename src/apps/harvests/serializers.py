from rest_framework import serializers

from apps.harvests.models import Harvest


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_apiary(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Authentication required.")
        if request and hasattr(request, 'user'):
            user = request.user
            if not user.apiarymembership_set.filter(
                    apiary_id=value.id,
                    role__in=['OWNER', 'EDITOR']
            ).exists():
                raise serializers.ValidationError("You do not have permission to create a harvest for this apiary.")
        return value
