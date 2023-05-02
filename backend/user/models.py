from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, verbose_name='login')
    first_name = models.CharField(max_length=20, verbose_name='first name')
    last_name = models.CharField(max_length=25, verbose_name='last name')
    birth_date = models.DateField()

    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

