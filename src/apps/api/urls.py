from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('apiaries/', include('apps.apiaries.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('hives/', include('apps.hives.urls')),
    path('admin/', admin.site.urls),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]
