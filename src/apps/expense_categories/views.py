from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.expense_categories.models import ExpenseCategory
from apps.expense_categories.serializers import ExpenseCategorySerializer


class ExpenseCategoryViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseCategorySerializer

    @extend_schema(
        summary='List all expense categories',
        description='Retrieve a list of all expense categories.',
        responses={
            200: ExpenseCategorySerializer(many=True),
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        categories = ExpenseCategory.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)
