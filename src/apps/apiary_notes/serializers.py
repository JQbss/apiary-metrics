from rest_framework import serializers

from apps.apiaries.models import Apiary
from apps.apiary_notes.models import ApiaryNote


class ApiaryNoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ApiaryNote
        fields = '__all__'
        read_only_fields = ['id']

    def validate_apiary(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Authentication required.")

        try:
            apiary = Apiary.objects.get(id=value.id)
        except Apiary.DoesNotExist:
            raise serializers.ValidationError("Apiary does not exist.")

        if request and hasattr(request, 'user'):
            user = request.user
            if not user.apiarymembership_set.filter(
                    apiary_id=apiary.id,
                    role__in=['OWNER', 'EDITOR']
            ).exists():
                raise serializers.ValidationError(
                    "You do not have permission to create a note for this apiary.")
        return value