import clearbit
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    site = models.URLField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6,
                              blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    CLEARBIT_FIELDS = ['bio', 'site', 'avatar', 'gender']

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_data_from_clearbit(self):
        clearbit_data = clearbit.Enrichment.find(email=self.email, stream=True)

        for field in self.CLEARBIT_FIELDS:
            if getattr(self, field):
                setattr(self, field, clearbit_data.get(field))

        self.save()
