from django.db import models


class HiveType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'hive_types'
        db_table = 'hive_types'
        verbose_name = 'Hive Type'
        verbose_name_plural = 'Hive Types'

    def __str__(self):
        return self.name