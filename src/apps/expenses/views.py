from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.expenses.models import Expense
from apps.expenses.serializers import ExpenseSerializer


class ExpensesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    @extend_schema(
        request=ExpenseSerializer,
        summary='Create a new expense',
        description='Create a new expense for the authenticated user',
        responses={
            201: ExpenseSerializer,
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
        summary='List all expenses',
        description='Retrieve a list of all expenses for the authenticated user',
        responses={
            200: ExpenseSerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        user = request.user
        expenses = user.expenses.all()
        serializer = self.serializer_class(expenses, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Retrieve an expense',
        description='Retrieve a specific expense for the authenticated user',
        responses={
            200: ExpenseSerializer,
            404: 'Not Found',
        },
    )
    def retrieve(self, request, pk=None):
        try:
            expense = request.user.expenses.get(pk=pk)
            serializer = self.serializer_class(expense)
            return Response(serializer.data)
        except Expense.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

    @extend_schema(
        request=ExpenseSerializer,
        summary='Update an expense',
        description='Update a specific expense for the authenticated user',
        responses={
            200: ExpenseSerializer,
            400: 'Bad Request',
            404: 'Not Found',
        },
    )
    def update(self, request, pk=None):
        try:
            expense = request.user.expenses.get(pk=pk)
            serializer = self.serializer_class(expense, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Expense.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

    @extend_schema(
        summary='Delete an expense',
        description='Delete a specific expense for the authenticated user',
        responses={
            204: 'No Content',
            404: 'Not Found',
        },
    )
    def destroy(self, request, pk=None):
        try:
            expense = request.user.expenses.get(pk=pk)
            expense.delete()
            return Response(status=204)
        except Expense.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)
