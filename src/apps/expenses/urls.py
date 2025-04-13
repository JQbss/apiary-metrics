from rest_framework.routers import SimpleRouter

from apps.expenses.views import ExpensesViewSet

app_name = 'expenses'
router = SimpleRouter()
router.register('', ExpensesViewSet, basename='expenses')
urlpatterns = router.urls