import clearbit
from django.apps import AppConfig
from django.conf import settings


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        clearbit.key = settings.CLEARBIT_KEY
