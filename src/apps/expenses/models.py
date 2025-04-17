from django.db import models
from django.conf import settings

from utils.fields import LowerCaseField


class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    cost = models.DecimalField(max_digits=10, decimal_places=2)
    category = LowerCaseField(max_length=255)
    date = models.DateField()
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'expenses'
        db_table = 'expenses'
        verbose_name = 'expense'
        verbose_name_plural = 'expenses'
        ordering = ['date']

    def __str__(self):
        return f'{self.user.email} - {self.category} - {self.cost}'
