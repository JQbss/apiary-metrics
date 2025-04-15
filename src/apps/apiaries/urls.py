from rest_framework.routers import SimpleRouter

from apps.apiaries.views import ApiariesViewSet

app_name='apiaries'
router = SimpleRouter()
router.register('', ApiariesViewSet, basename='apiaries')
urlpatterns = router.urls