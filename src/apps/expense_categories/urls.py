from rest_framework.routers import SimpleRouter

from apps.expense_categories.views import ExpenseCategoryViewSet

app_name = 'expense_categories'
router = SimpleRouter()
router.register('', ExpenseCategoryViewSet, basename='expense_categories')
urlpatterns = router.urls
