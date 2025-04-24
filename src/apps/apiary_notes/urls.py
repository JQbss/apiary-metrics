from rest_framework.routers import SimpleRouter

from apps.apiary_notes.views import ApiaryNotesViewSet

app_name = 'apiary_notes'
router = SimpleRouter()
router.register('', ApiaryNotesViewSet, basename='apiary-notes')
urlpatterns = router.urls