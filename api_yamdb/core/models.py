from django.db import models

from api_yamdb.constants import MAX_NAME_LENGTH


class BaseReviewModel(models.Model):
    text = models.TextField(verbose_name="Текст обзора")
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True


class BaseNameModel(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=MAX_NAME_LENGTH
    )

    class Meta:
        abstract = True
