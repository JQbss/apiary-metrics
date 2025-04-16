from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.apiaries.models import Apiary
from apps.hives.serializers import HiveSerializer


class HivesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HiveSerializer

    def get_queryset(self):
        user = self.request.user
        return self.serializer_class.Meta.model.objects.filter(apiary__user=user)

    @extend_schema(
        summary='Create a new hive',
        description='Create a new hive for existing apiary',
        responses={
            201: HiveSerializer,
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
        summary='Retrieve a hive',
        description='Retrieve a specific hive for the authenticated user',
        responses={
            200: HiveSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            hive = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=hive.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR', 'VIEWER']
            ).exists():
                return Response({'detail': 'You do not have permission to access this hive.'}, status=403)

            serializer = self.serializer_class(
                hive,
                context={'request': request}
            )
            return Response(serializer.data)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Hive not found'}, status=404)

    @extend_schema(
        summary='Update a hive',
        description='Update a specific hive for the authenticated user',
        responses={
            200: HiveSerializer,
            400: 'Bad Request',
            403: 'Forbidden',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            hive = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=hive.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR']
            ).exists():
                return Response({'detail': 'You do not have permission to access this hive.'}, status=403)

            serializer = self.serializer_class(
                hive,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Hive not found'}, status=404)

    @extend_schema(
        summary='Delete a hive',
        description='Delete a specific hive for the authenticated user',
        responses={
            204: 'No Content',
            403: 'Forbidden',
            404: 'Not Found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            hive = self.serializer_class.Meta.model.objects.get(pk=pk)
            if not request.user.apiarymembership_set.filter(
                    apiary_id=hive.apiary.id,
                    role__in=['ADMIN', 'OWNER', 'EDITOR']
            ).exists():
                return Response({'detail': 'You do not have permission to access this hive.'}, status=403)

            hive.delete()
            return Response(status=204)
        except self.serializer_class.Meta.model.DoesNotExist:
            return Response({'detail': 'Hive not found'}, status=404)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='apiary_id',
                type=int,
                description='Filter hives by apiary ID',
                required=False,
            ),
        ],
        summary='List of hives',
        description='Retrieve a list of hives by apiary ID or all hives for the authenticated user',
        responses={
            200: HiveSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        apiary_id = request.query_params.get('apiary_id')

        if apiary_id:
            try:
                apiary = Apiary.objects.get(
                    id=apiary_id,
                    users=request.user
                )
                hives = self.serializer_class.Meta.model.objects.filter(apiary=apiary)
            except Apiary.DoesNotExist:
                return Response({'detail': 'You do not have permission to access this apiary.'}, status=403)
        else:
            hives = self.serializer_class.Meta.model.objects.filter(
                apiary__users=request.user
            )

        hives = hives.select_related('apiary')

        serializer = self.serializer_class(hives, many=True, context={'request': request})
        return Response(serializer.data)
