from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.hive_inspections.serializers import HiveInspectionSerializers
from apps.hives.models import Hive


class HiveInspectionsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HiveInspectionSerializers

    def get_queryset(self):
        user = self.request.user
        return self.serializer_class.Meta.model.objects.filter(hive__apiary__user=user).select_related('hive__apiary')

    @extend_schema(
        summary='Create a new hive inspection',
        description='Create a new hive inspection for existing hive',
        responses={
            201: HiveInspectionSerializers,
            400: 'Bad Request',
        },
    )
    def create(self, request):
        print("Request data:", request.data)
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
        summary='List all hive inspections',
        description='Retrieve a list of all hive inspections for the authenticated user',
        responses={
            200: HiveInspectionSerializers(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        hive_id = request.query_params.get('hive_id')
        print ("user request", request.user)
        if hive_id:
            try:
                hive = Hive.objects.get(
                    id=hive_id,
                    apiary__users=request.user
                )
                hive_inspections = self.serializer_class.Meta.model.objects.filter(hive=hive)
            except Hive.DoesNotExist:
                return Response({'detail': 'Hive not found'}, status=404)
        else:
            hive_inspections = self.serializer_class.Meta.model.objects.filter(
                hive__apiary__users=request.user
            )

        hive_inspections = hive_inspections.select_related('hive__apiary')
        serializer = self.serializer_class(
            hive_inspections,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve a hive inspection',
        description='Retrieve a specific hive inspection for the authenticated user',
        responses={
            200: HiveInspectionSerializers(many=True),
            401: 'Unauthorized',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            hive_inspection = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=hive_inspection.hive.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({'detail': 'You do not have permission to access this hive inspection.'}, status=403)

            serializer = self.serializer_class(
                hive_inspection,
                context={'request': request}
            )
            return Response(serializer.data)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Hive inspection not found'}, status=404)

    @extend_schema(
        summary='Update a hive inspection',
        description='Update a specific hive inspection for the authenticated user',
        responses={
            200: HiveInspectionSerializers,
            400: 'Bad Request',
        },
    )
    def update(self, request, pk=None):
        try:
            hive_inspection = self.serializer_class.Meta.model.objects.get(pk=pk)
            serializer = self.serializer_class(
                hive_inspection,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Hive inspection not found'}, status=404)
