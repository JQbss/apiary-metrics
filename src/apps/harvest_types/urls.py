from rest_framework.routers import SimpleRouter

from apps.harvest_types.views import HarvestTypeViewSet

app_name = 'harvest_types'
router = SimpleRouter()
router.register('', HarvestTypeViewSet, basename='harvest_types')
urlpatterns = router.urls