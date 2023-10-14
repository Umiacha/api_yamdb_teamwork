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
    email = models.CharField('Почта', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=150,
                            default='user', choices=USERS_ROLES)
    
    def clean_is_staff(self) -> None:
        if self.role == 'admin' or self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = False
        return super().clean()

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# 1) Установить simple-jwt и переделать, если необходимо.
# 2) Установить валидацию по регулярному выражению для CustomUser.username
# 3) Исправить json, выдаваемый на users/me.
# 4) Проверить пермишены в действии.


# 5) Проект переставлен на русский язык, поэтому надо сделать локализацию для всех своих моделей и полей.
# 6) Установить получение confirmation_code по почте.
