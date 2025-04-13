from django.db import models
from django.conf import settings

class Expense(models.Model):
    class Category(models.TextChoices):
        BEES = 'BEES', 'Bees'
        BEESWAX = 'BEESWAX', 'Beeswax'
        FOOD = 'FOOD', 'Food'
        QUEEN = 'QUEEN', 'Queen'
        TRANSPORT = 'TRANSPORT', 'Transport'
        UTILITIES = 'UTILITIES', 'Utilities'
        OTHER = 'OTHER', 'Other'


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
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
        return f'{self.user.email} - {self.category} - {self.amount}'