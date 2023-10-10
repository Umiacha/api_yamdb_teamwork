from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)],
    )
    rating = models.IntegerField(
        'Рейтинг произведения', default=0
    )
    description  = models.TextField(
        'Описание',
        null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Slug жанра',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category, verbose_name='Slug категории',
        null=True, on_delete=models.SET_NULL,
        related_name='titles'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        null=True
    )
