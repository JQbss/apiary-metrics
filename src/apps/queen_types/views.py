from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from apps.queen_types.models import QueenType
from apps.queen_types.serializers import QueenTypeSerializer


class QueenTypesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QueenTypeSerializer

    @extend_schema(
        summary='Get all queen types',
        description='Retrieve a list of all queen types',
        responses={
            200: QueenTypeSerializer(many=True),
            401: 'Unauthorized',
        }
    )
    def list(self, request):
        queen_types = QueenType.objects.all()
        serializer = self.serializer_class(queen_types, many=True)
        return Response(serializer.data)
