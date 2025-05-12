from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.apiaries.models import Apiary
from apps.harvests.models import Harvest
from apps.harvests.serializers import HarvestSerializer
from apps.hives.models import Hive


class HarvestsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HarvestSerializer

    @extend_schema(
        summary='Create a new harvest',
        description='Create a new harvest for existing apiary',
        responses={
            201: HarvestSerializer,
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
        summary='Retrieve a harvest',
        description='Retrieve a specific harvest for the authenticated user',
        responses={
            200: HarvestSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            harvest = Harvest.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=harvest.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({'detail': 'You do not have permission to access this harvest.'}, status=403)
            serializer = self.serializer_class(
                harvest,
                context={'request': request}
            )
            return Response(serializer.data)
        except Hive.DoesNotExist:
            return Response({'detail': 'Harvest not found'}, status=404)

    @extend_schema(
        summary='Update a harvest',
        description='Update an existing harvest for the authenticated user',
        responses={
            200: HarvestSerializer,
            400: 'Bad Request',
            403: 'Forbidden',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            harvest = self.serializer_class.Meta.model.objects.get(pk=pk)
            serializer = self.serializer_class(
                harvest,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Harvest not found'}, status=404)

    @extend_schema(
        summary='Delete a harvest',
        description='Delete an existing harvest for the authenticated user',
        responses={
            204: 'No Content',
            403: 'Forbidden',
            404: 'Not Found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            harvest = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=harvest.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR']
            ).exists():
                return Response({'detail': 'You do not have permission to delete this harvest.'}, status=403)
            harvest.delete()
            return Response(status=204)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Harvest not found'}, status=404)

    @extend_schema(
        summary='List all harvests',
        description='Retrieve a list of all harvests for the authenticated user',
        parameters=[
            OpenApiParameter(
                name='apiary_id',
                type=int,
                description='Filter by apiary ID',
                required=False,
            )
        ],
        responses={
            200: HarvestSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        apiary_id = request.query_params.get('apiary_id')
        if apiary_id:
            try:
                apiary = Apiary.objects.get(
                    id=apiary_id,
                    users=request.user,
                )
                harvests = self.serializer_class.Meta.model.objects.filter(apiary=apiary)
            except Apiary.DoesNotExist:
                return Response({'detail': 'You do not have permission to access this apiary.'}, status=403)
        else:
            harvests = self.serializer_class.Meta.model.objects.filter(
                apiary__users=request.user
            )

        harvests = harvests.select_related('apiary')
        serializer = self.serializer_class(
            harvests,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
