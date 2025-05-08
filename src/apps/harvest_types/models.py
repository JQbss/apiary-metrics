from django.db import models

class HarvestType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'harvest_types'
        db_table = 'harvest_types'
        verbose_name = 'Harvest Type'
        verbose_name_plural = 'Harvest Types'

    def __str__(self):
        return self.name