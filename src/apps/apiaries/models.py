from django.conf import settings
from django.db import models


# Create your models here.
class ApiaryRole(models.TextChoices):
    OWNER = 'OWNER', 'Owner'
    EDITOR = 'EDITOR', 'Editor'
    VIEWER = 'VIEWER', 'Viewer'


class Apiary(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ApiaryMembership',
        related_name='apiaries'
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    coordination_latitude = models.FloatField(blank=True, null=True)
    coordination_longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apiaries'
        db_table = 'apiaries'
        verbose_name = 'apiary'
        verbose_name_plural = 'apiaries'

    def __str__(self):
        return self.name


class ApiaryMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    apiary = models.ForeignKey(
        Apiary,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=ApiaryRole.choices,
        default=ApiaryRole.OWNER
    )

    class Meta:
        app_label = 'apiaries'
        db_table = 'apiaries_membership'
        unique_together = ('user', 'apiary')

    def __str__(self):
        return f'{self.user.email} - {self.apiary.name} - {self.role}'
