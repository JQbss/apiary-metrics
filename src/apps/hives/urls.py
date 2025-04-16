from rest_framework.routers import SimpleRouter

from apps.hives.views import HivesViewSet

app_name = 'hives'
router = SimpleRouter()
router.register('', HivesViewSet, basename='hives')
urlpatterns = router.urls
