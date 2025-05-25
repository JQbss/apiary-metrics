from rest_framework.routers import SimpleRouter

from apps.sale_types.views import SaleTypesViewSet

app_name = 'sale_types'
router = SimpleRouter()
router.register('', SaleTypesViewSet, basename='sale_types')
urlpatterns = router.urls
