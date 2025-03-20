from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import RegisterViewSet, UserProfileViewSet

app_name = 'users'
router = SimpleRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('profile', UserProfileViewSet, basename='profile')
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
