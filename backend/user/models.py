from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .managers import CustomUserManager


class User(AbstractBaseUser):
    login = models.CharField(max_length=50, unique=True, verbose_name='login')
    first_name = models.CharField(max_length=20, verbose_name='first name')
    last_name = models.CharField(max_length=25, verbose_name='last name')
    birth_date = models.DateField()

    # User.objects.create_user(login=login, birth_date=birth_date, first_name=first_name, last_name=last_name)

    objects = CustomUserManager()

    USERNAME_FIELD = "login"

    def __str__(self):
        return self.login

    # @property
    # def is_staff(self):
    #     return self.is_admin

