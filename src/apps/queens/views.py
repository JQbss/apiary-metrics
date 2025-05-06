from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.hives.models import Hive
from apps.queens.serializers import QueenSerializer


class QueensViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QueenSerializer

    def get_queryset(self):
        user = self.request.user
        return self.serializer_class.Meta.model.objects.filter(hive__apiary__user=user).select_related('hive__apiary')

    @extend_schema(
        summary='Create a new queen',
        description='Create a new queen for existing hive',
        responses={
            201: QueenSerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='hive_id',
                type=int,
                description='Filter by hive ID',
                required=False,
            )
        ],
        summary='List all queens',
        description='Retrieve a list of all queens for the authenticated user',
        responses={
            200: QueenSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        hive_id = request.query_params.get('hive_id')
        if hive_id:
            try:
                hive = Hive.objects.get(
                    id=hive_id,
                    apiary__users=request.user
                )
                queens = self.serializer_class.Meta.model.objects.filter(hive=hive)
            except Hive.DoesNotExist:
                return Response({"detail": "Hive not found."}, status=404)
        else:
            queens = self.serializer_class.Meta.model.objects.filter(
                hive__apiary__users=request.user
            )

        queens = queens.select_related('hive__apiary')
        serializer = self.serializer_class(
            queens,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve a queen',
        description='Retrieve a specific queen by ID',
        responses={
            200: QueenSerializer,
            404: 'Not Found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            queen = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=queen.hive.apiary_id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({"detail": "You do not have permission to get details about this queen."}, status=404)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({"detail": "Queen not found."}, status=404)

    @extend_schema(
        summary='Update a queen',
        description='Update a specific queen by ID',
        responses={
            200: QueenSerializer,
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            queen = self.serializer_class.Meta.model.objects.get(pk=pk)
            serializer = self.serializer_class(
                queen,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({"detail": "Queen not found."}, status=404)
