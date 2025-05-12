from rest_framework.routers import SimpleRouter

from apps.harvests.views import HarvestsViewSet

app_name = 'harvests'
router = SimpleRouter()
router.register('', HarvestsViewSet, basename='harvests')
urlpatterns = router.urls