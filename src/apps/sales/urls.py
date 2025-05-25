from rest_framework.routers import SimpleRouter

from apps.sales.views import SaleViewSet

app_name = 'sales'
router = SimpleRouter()
router.register('', SaleViewSet, basename='sales')
urlpatterns = router.urls
