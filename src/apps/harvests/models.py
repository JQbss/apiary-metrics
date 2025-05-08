from django.db import models

from utils.fields import UnitField, LowerCaseField


class Harvest(models.Model):
    apiary = models.ForeignKey(
        'apiaries.Apiary',
        on_delete=models.CASCADE,
        related_name='harvests'
    )
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(choices=UnitField.choices)
    type = LowerCaseField(max_length=255, default='other')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'harvests'
        db_table = 'harvests'
        verbose_name = 'harvest'
        verbose_name_plural = 'harvests'

    def __str__(self):
        return f'{self.apiary.name} - {self.type} - {self.amount} {self.unit}'
