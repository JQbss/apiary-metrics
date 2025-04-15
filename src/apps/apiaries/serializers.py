from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.apiaries.models import ApiaryRole, Apiary, ApiaryMembership

User = get_user_model()


class ApiaryMembershipSerializer(serializers.ModelSerializer):
    user = User
    role = serializers.ChoiceField(
        choices=ApiaryRole.choices,
        default=ApiaryRole.OWNER
    )

    class Meta:
        model = ApiaryMembership
        fields = ['id', 'user', 'role']
        read_only_fields = ['user']


class ApiaryMembershipAddUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=ApiaryRole.choices,
        default=ApiaryRole.VIEWER
    )

    class Meta:
        model = ApiaryMembership
        fields = ['email', 'role']
        read_only_fields = ['id']

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return user

    def validate_role(self, value):
        if value == ApiaryRole.OWNER:
            raise serializers.ValidationError("Cannot assign OWNER role.")
        if value not in ApiaryRole.values:
            raise serializers.ValidationError("Invalid role.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        role = validated_data['role']
        apiary = self.context['apiary']
        user = User.objects.get(email=email)

        if ApiaryMembership.objects.filter(user=user, apiary=apiary).exists():
            raise serializers.ValidationError("User is already a member of this apiary.")

        membership = ApiaryMembership.objects.create(
            user=user,
            apiary=apiary,
            role=role
        )
        return membership

    def to_representation(self, instance):
        return ApiaryMembershipSerializer(instance).data


class ApiarySerializer(serializers.ModelSerializer):
    members = ApiaryMembershipSerializer('apiarymembership_set', many=True, read_only=True)

    class Meta:
        model = Apiary
        fields = ['id', 'name', 'location', 'coordination_latitude', 'coordination_longitude', 'created_at',
                  'updated_at', 'members']
        read_only_fields = ['id', 'created_at', 'updated_at']
