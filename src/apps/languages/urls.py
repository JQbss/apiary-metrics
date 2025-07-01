from rest_framework.routers import SimpleRouter

from apps.languages.views import LanguageViewSet

app_name = 'languages'
router = SimpleRouter()
router.register('', LanguageViewSet, basename='languages')
urlpatterns = router.urls
