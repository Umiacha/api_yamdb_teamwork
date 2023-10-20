from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UsersConfig(AppConfig):
    name = "users"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        @receiver(pre_save, sender="users.CustomUser")
        def is_user_staff_or_not(sender, instance, **kwargs):
            instance.clean_is_staff()
