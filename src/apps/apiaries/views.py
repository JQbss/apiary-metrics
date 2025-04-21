from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.apiaries.models import ApiaryMembership, ApiaryRole
from apps.apiaries.serializers import ApiarySerializer, ApiaryMembershipAddUserSerializer


class ApiariesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ApiarySerializer

    @extend_schema(
        request=ApiarySerializer,
        summary='Create a new apiary',
        description='Create a new apiary for the authenticated user',
        responses={
            201: ApiarySerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            apiary = serializer.save()
            ApiaryMembership.objects.create(
                user=request.user,
                apiary=apiary,
                role=ApiaryRole.OWNER,
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary='List all apiaries',
        description='Retrieve a list of all apiaries for the authenticated user',
        responses={
            200: ApiarySerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        user = request.user
        apiaries = user.apiaries.all()
        serializer = self.serializer_class(apiaries, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve an apiary',
        description='Retrieve a specific apiary for the authenticated user',
        responses={
            200: ApiarySerializer,
            404: 'Not Found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            apiary = request.user.apiaries.get(pk=pk)
        except ApiaryMembership.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.serializer_class(apiary)
        return Response(serializer.data)

    @extend_schema(
        summary='Update an apiary',
        description='Update a specific apiary for the authenticated user',
        responses={
            200: ApiarySerializer,
            400: 'Bad Request',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            apiary = request.user.apiaries.get(pk=pk)
        except ApiaryMembership.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.serializer_class(apiary, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary='Delete an apiary',
        description='Delete a specific apiary for the authenticated user',
        responses={
            204: 'No Content',
            404: 'Not Found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            apiary = request.user.apiaries.get(pk=pk)
        except ApiaryMembership.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        apiary.delete()
        return Response(status=204)

    @extend_schema(
        summary='Add a member to an apiary',
        description='Add a new member to an apiary',
        request=ApiaryMembershipAddUserSerializer,
        responses={
            201: ApiaryMembershipAddUserSerializer,
            400: 'Bad Request',
            403: 'Forbidden',
            404: 'Not Found',
        },
    )
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        try:
            apiary = request.user.apiaries.get(pk=pk)
            membership = ApiaryMembership.objects.filter(
                user=request.user,
                apiary=apiary,
                role=ApiaryRole.OWNER
            ).first()
            if not membership:
                return Response({'detail': 'Forbidden.'}, status=403)
        except ApiaryMembership.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = ApiaryMembershipAddUserSerializer(
            data=request.data,
            context={'apiary': apiary}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
