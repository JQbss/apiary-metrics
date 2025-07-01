from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.languages.models import Language


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='email')
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='first name')
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='last name')
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='avatar')
    language = models.OneToOneField(Language, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='language')
    

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
