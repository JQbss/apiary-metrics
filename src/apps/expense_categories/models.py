from django.db import models


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'expense_categories'
        db_table = 'expense_categories'
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name
