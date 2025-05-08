from django.contrib import admin

from apps.harvest_types.models import HarvestType


@admin.register(HarvestType)
class HarvestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
