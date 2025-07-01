from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'languages'
        verbose_name = 'language'
        verbose_name_plural = 'languages'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"
