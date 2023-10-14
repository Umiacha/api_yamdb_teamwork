import time

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


USERS_ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]

def check_name(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя создать пользователя с никнеймом "me"!'
        )


class CustomUser(AbstractUser):
    username = models.CharField('Никнейм', max_length=150,
                                unique=True, validators=[check_name, RegexValidator(regex='^[\w.@+-]+\Z')])
    email = models.EmailField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=150,
                            default='user', choices=USERS_ROLES)
    confirmation_code = models.CharField('Код подтверждения', max_length=150, blank=True)
    
    def clean_is_staff(self) -> None:
        if self.role == 'admin' or self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = False
        return super().clean()
    
    def create_confirmation_code(self):
        """
        Create, set for user instance and return confirmation code.
        """
        self.confirmation_code = str(int(time.time()))
        self.save()
        return self.confirmation_code

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
