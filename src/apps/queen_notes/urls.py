from rest_framework.routers import SimpleRouter

from apps.queen_notes.views import QueenNotesViewSet

app_name = 'queen_notes'
router = SimpleRouter()
router.register('', QueenNotesViewSet, basename='queen-notes')
urlpatterns = router.urls