from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CustomUser


@receiver(pre_save, sender=CustomUser)
def is_user_staff_or_not(instance, **kwargs):
    instance.clean_is_staff()
