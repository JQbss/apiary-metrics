from django.db import models
from utils.fields import LowerCaseField


class HiveAggression(models.TextChoices):
    VERY_LOW = 'VERY_LOW', 'Very Low'
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    VERY_HIGH = 'VERY_HIGH', 'Very High'


class HiveStrength(models.TextChoices):
    VERY_WEAK = 'VERY_WEAK', 'Very Weak'
    WEAK = 'WEAK', 'Weak'
    MEDIUM = 'MEDIUM', 'Medium'
    STRONG = 'STRONG', 'Strong'
    VERY_STRONG = 'VERY_STRONG', 'Very Strong'


class Hive(models.Model):
    apiary = models.ForeignKey(
        'apiaries.Apiary',
        on_delete=models.CASCADE,
        related_name='hives'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = LowerCaseField(max_length=255, default='other')
    aggression = models.CharField(
        max_length=20,
        choices=HiveAggression.choices,
        default=HiveAggression.MEDIUM
    )
    strength = models.CharField(
        max_length=20,
        choices=HiveStrength.choices,
        default=HiveStrength.MEDIUM
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'hives'
        db_table = 'hives'
        verbose_name = 'hive'
        verbose_name_plural = 'hives'

    def __str__(self):
        return f'{self.apiary.name} - {self.name}'
