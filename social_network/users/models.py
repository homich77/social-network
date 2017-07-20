import clearbit
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.tasks import fill_user_data


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        fill_user_data.delay(user.pk)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


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
