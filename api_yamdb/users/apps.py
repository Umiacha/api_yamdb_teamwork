from django.apps import AppConfig
from django.core.signals import request_finished


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import is_user_staff_or_not

        request_finished.connect(
            is_user_staff_or_not,
            sender='users.CustomUser',
            dispatch_uid='unique_id'
        )
