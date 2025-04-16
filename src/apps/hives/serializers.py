import rest_framework.serializers as serializers
from apps.hives.models import Hive


class HiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

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
                raise serializers.ValidationError("You do not have permission to create a hive for this apiary.")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Hive name cannot be empty.")
        return value

class HiveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hive
        fields = 'apiary'
