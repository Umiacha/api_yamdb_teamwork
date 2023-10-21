import time

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.constants import (
    MAX_USERNAME_ROLE_CODE_LENGTH,
    MAX_EMAIL_LENGTH, USER,
    MODERATOR, ADMIN
)

USERS_ROLES = [
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
]


def check_name(value):
    lower_value = value.lower()
    if lower_value == 'me':
        raise ValidationError(
            f'Нельзя создать пользователя с никнеймом {value}!'
        )


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name="Никнейм",
        max_length=MAX_USERNAME_ROLE_CODE_LENGTH,
        unique=True,
        validators=[check_name, RegexValidator(regex=r"^[\w.@+-]+\Z")],
    )
    password = models.CharField('Ненужный пароль', max_length=128, blank=True)
    email = models.EmailField(
        verbose_name="Почта", max_length=MAX_EMAIL_LENGTH, unique=True
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(
        verbose_name="Роль",
        max_length=MAX_USERNAME_ROLE_CODE_LENGTH,
        default="user",
        choices=USERS_ROLES,
    )
    confirmation_code = models.CharField(
        verbose_name="Код подтверждения",
        max_length=MAX_USERNAME_ROLE_CODE_LENGTH,
        blank=True,
    )
    is_admin = models.BooleanField(
        verbose_name="Является администратором",
        default=False,
    )
    is_moderator = models.BooleanField(
        verbose_name="Является модератором",
        default=False
    )

    def pre_save(self):
        if self.role == ADMIN or self.is_superuser:
            self.is_admin = True
            self.is_staff = True
            self.is_moderator = False
        elif self.role == MODERATOR:
            self.is_moderator = True
            self.is_admin = False
            self.is_staff = False
        else:
            self.is_moderator = False
            self.is_admin = False
            self.is_staff = False
        self.full_clean()

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

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
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)
