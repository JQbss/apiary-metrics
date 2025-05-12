from rest_framework.routers import SimpleRouter

from apps.hive_types.views import HiveTypesViewSet

app_name = 'hive_types'
router = SimpleRouter()
router.register('', HiveTypesViewSet, basename='hive_types')
urlpatterns = router.urls
