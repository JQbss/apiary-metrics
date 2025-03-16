from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='email')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ROLES = {
        ('admin', 'Admin'),
        ('beekeeper', 'Beekeeper'),
        ('viewer', 'Viewer'),
    }

    role = models.CharField(max_length=20, choices=ROLES, default='beekeeper')

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username