from django.conf import settings
from django.db import models

from utils.fields import UnitField


class Sale(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales'
    )
    date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    prize = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(choices=UnitField.choices)
    type = models.CharField(max_length=255, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'sales'
        db_table = 'sales'
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return f'{self.user.email} - {self.type} - {self.quantity} {self.unit}'
