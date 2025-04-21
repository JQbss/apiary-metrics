from django.db import models

class HiveInspection(models.Model):
    hive = models.ForeignKey(
        'hives.Hive',
        on_delete=models.CASCADE,
        related_name='inspections'
    )
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'hive_inspections'
        db_table = 'hive_inspections'
        verbose_name = 'hive inspection'
        verbose_name_plural = 'hive inspections'
        ordering = ['date']

    def __str__(self):
        return f'{self.hive.apiary.name} - {self.hive.name} - {self.date}'