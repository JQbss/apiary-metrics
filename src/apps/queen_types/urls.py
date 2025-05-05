from rest_framework.routers import SimpleRouter

from apps.queen_types.views import QueenTypesViewSet

app_name = 'queen_types'
router = SimpleRouter()
router.register('', QueenTypesViewSet, basename='queen_types')
urlpatterns = router.urls
