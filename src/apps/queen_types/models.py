from django.db import models


class QueenType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'queen_types'
        db_table = 'queen_types'
        verbose_name = 'Queen Type'
        verbose_name_plural = 'Queen Types'

    def __str__(self):
        return self.name
