from rest_framework.routers import SimpleRouter

from apps.queens.views import QueensViewSet

app_name = 'queens'
router = SimpleRouter()
router.register('', QueensViewSet, basename='queens')
urlpatterns = router.urls