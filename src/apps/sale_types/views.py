from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.sale_types.models import SaleType
from apps.sale_types.serializers import SaleTypeSerializer


class SaleTypesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleTypeSerializer

    @extend_schema(
        summary='Get all sale types',
        description='Retrieve a list of all sale types',
        responses={
            200: SaleTypeSerializer(many=True),
            401: 'Unauthorized',
        }
    )
    def list(self, request):
        queryset = SaleType.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
