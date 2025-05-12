from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.harvest_types.models import HarvestType
from apps.harvest_types.serializers import HarvestTypeSerializer


class HarvestTypeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HarvestTypeSerializer

    @extend_schema(
        summary='Get all harvest types',
        description='Retrieve a list of all harvest types',
        responses={
            200: HarvestTypeSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        harvest_types = HarvestType.objects.all()
        serializer = self.serializer_class(harvest_types, many=True)
        return Response(serializer.data)