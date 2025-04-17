from django.db import models
from utils.fields import LowerCaseField


class Hive(models.Model):
    apiary = models.ForeignKey(
        'apiaries.Apiary',
        on_delete=models.CASCADE,
        related_name='hives'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = LowerCaseField(max_length=255, default='other')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'hives'
        db_table = 'hives'
        verbose_name = 'hive'
        verbose_name_plural = 'hives'

    def __str__(self):
        return f'{self.apiary.name} - {self.name}'
