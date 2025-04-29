from django.db import models

from utils.fields import LowerCaseField


class Queen(models.Model):
    hive = models.ForeignKey(
        'hives.Hive',
        on_delete=models.CASCADE,
        related_name='queens'
    )
    date = models.DateField()
    is_active = models.BooleanField(default=False)
    type = LowerCaseField(max_length=255, default='other')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'queens'
        db_table = 'queens'
        verbose_name = 'queen'
        verbose_name_plural = 'queens'
        ordering = ['-date']

    def __str__(self):
        return f'{self.hive.apiary.name} - {self.hive.name} - {self.date}'