from rest_framework.routers import SimpleRouter

from apps.hive_inspections.views import HiveInspectionsViewSet

app_name = 'hive_inspections'
router = SimpleRouter()
router.register('', HiveInspectionsViewSet, basename='hive-inspections')
urlpatterns = router.urls