from django.contrib import admin

from apps.hive_types.models import HiveType


@admin.register(HiveType)
class HiveTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
