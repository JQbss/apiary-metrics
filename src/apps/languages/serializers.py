from rest_framework import serializers

from apps.languages.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_code(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Language code must contain only alphabetic characters.")
        return value.lower()

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Language name cannot be empty.")
        return value.strip()
