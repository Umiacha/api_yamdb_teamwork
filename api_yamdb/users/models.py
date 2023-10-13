from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def check_name(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя создать пользователя с никнеймом "me"!'
        )


class CustomUser(AbstractUser):
    USERS_ROLES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    username = models.CharField('Никнейм', max_length=150,
                                unique=True, validators=[check_name])
    email = models.CharField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=150,
                            default='user', choices=USERS_ROLES)

    def __str__(self):
        return self.username
