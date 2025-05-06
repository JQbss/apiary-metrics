from rest_framework import serializers

from apps.queen_notes.models import QueenNote
from apps.queens.models import Queen


class QueenNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueenNote
        fields = '__all__'
        read_only_fields = ['id']

    def validate_queen(self, value):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Authentication required.")

        try:
            queen = Queen.objects.get(id=value.id)
        except Queen.DoesNotExist:
            raise serializers.ValidationError("Queen does not exist.")

        if request and hasattr(request, 'user'):
            user = request.user
            if not user.apiarymembership_set.filter(
                    apiary_id=queen.hive.apiary.id,
                    role__in=['OWNER', 'EDITOR']
            ).exists():
                raise serializers.ValidationError(
                    "You do not have permission to create a queen note for this queen.")
        return value
