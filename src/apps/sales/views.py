from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from apps.sales.models import Sale
from apps.sales.serializers import SaleSerializer


class SaleViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SaleSerializer

    @extend_schema(
        request=SaleSerializer,
        summary='Create a new sale',
        description='Create a new sale for the authenticated user',
        responses={
            201: SaleSerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary='List all sales',
        description='Retrieve a list of all sales for the authenticated user',
        responses={
            200: SaleSerializer(many=True),
        },
    )
    def list(self, request):
        sales = request.user.sales.all()
        serializer = self.serializer_class(sales, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve a sale',
        description='Retrieve a specific sale by its ID',
        responses={
            200: SaleSerializer,
            404: 'Not Found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            sale = request.user.sales.get(pk=pk)
            serializer = self.serializer_class(sale)
            return Response(serializer.data)
        except Sale.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

    @extend_schema(
        summary='Update a sale',
        description='Update a specific sale by its ID',
        request=SaleSerializer,
        responses={
            200: SaleSerializer,
            400: 'Bad Request',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            sale = request.user.sales.get(pk=pk)
            serializer = self.serializer_class(sale, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Sale.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

    @extend_schema(
        summary='Delete a sale',
        description='Delete a specific sale by its ID',
        responses={
            204: 'No Content',
            404: 'Not Found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            sale = request.user.sales.get(pk=pk)
            sale.delete()
            return Response(status=204)
        except Sale.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
