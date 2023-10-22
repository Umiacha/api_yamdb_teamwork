import re

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_username(value):
    """Валидация для API"""
    pattern = re.compile(r'^[\w.@+-]+\Z')
    if value.lower() != "me" and pattern.match(value):
        return value
    raise serializers.ValidationError


def check_name(value):
    """Валидация для модели и shell"""
    lower_value = value.lower()
    if lower_value == "me":
        raise ValidationError(
            f"Нельзя создать пользователя с никнеймом {value}!"
        )
