from django.db import models


class SaleType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'sale_types'
        db_table = 'sale_types'
        verbose_name = 'Sale Type'
        verbose_name_plural = 'Sale Types'

    def __str__(self):
        return self.name
