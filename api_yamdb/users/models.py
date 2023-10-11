from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


"""
Куча информации: можно настраивать права групп пользователей через Django.
Однако проблема, что в полях User должны быть role и bio (их нет в auth_user).

В таком случае надо понять:
1) Просто создать CustomUser(django.contrib.auth.User) и добавить ему два поля дополнительно?  <-- Да
2) Как обеспечить role='admin' для суперпользователя при любых обстоятельствах?  <-- В permissions делать проверку user.is_superuser == True
3) Как контролировать доступ пользователей к разным действиям, учитывая, что у нас куча эндпоинтов:
задать Permissions и Group исходя из role пользователя или просто написать пермишены из drf?
Пока что думаю, что ограничение на проект -- IsAuthenticatedOrReadonly (ограничения на анонимов).
"""

def check_name(value):
    if value == 'me':
        raise ValidationError('Нельзя создать пользователя с никнеймом "me"!')


class CustomUser(AbstractUser):
    USERS_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    username = models.CharField('Никнейм', max_length=150, unique=True, validators=[check_name])
    email = models.CharField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=150, default='user', choices=USERS_ROLES)
