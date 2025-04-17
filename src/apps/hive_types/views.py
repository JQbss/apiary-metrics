from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.hive_types.models import HiveType
from apps.hive_types.serializers import HiveTypeSerializers


class HiveTypesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HiveTypeSerializers

    @extend_schema(
        summary='List all hive types',
        description='Retrieve a list of all hive types.',
        responses={
            200: HiveTypeSerializers(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        hive_types = HiveType.objects.all()
        serializer = self.serializer_class(hive_types, many=True)
        return Response(serializer.data)
