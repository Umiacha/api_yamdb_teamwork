from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UsersConfig(AppConfig):
    name = "users"
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Пользователи"
