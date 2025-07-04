from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('apiaries/', include('apps.apiaries.urls')),
    path('apiary_notes/', include('apps.apiary_notes.urls')),
    path('harvests/', include('apps.harvests.urls')),
    path('harvest_types/', include('apps.harvest_types.urls')),
    path('queens/', include('apps.queens.urls')),
    path('queen_notes/', include('apps.queen_notes.urls')),
    path('queen_types/', include('apps.queen_types.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('expense_categories/', include('apps.expense_categories.urls')),
    path('sales/', include('apps.sales.urls')),
    path('sale_types/', include('apps.sale_types.urls')),
    path('hives/', include('apps.hives.urls')),
    path('hive_inspections/', include('apps.hive_inspections.urls')),
    path('hive_types/', include('apps.hive_types.urls')),
    path('languages/', include('apps.languages.urls')),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]
