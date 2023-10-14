from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField("Slug категории", unique=True, max_length=50)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField("Slug жанра", unique=True, max_length=50)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField(
        "Год выпуска",
        validators=[MaxValueValidator(timezone.now().year)],
    )
    rating = models.FloatField("Рейтинг произведения", default=0.0)
    description = models.TextField("Описание", blank=True, default="")
    genre = models.ManyToManyField(
        Genre, verbose_name="Slug жанра", through="GenreTitle"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Slug категории",
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name="ID произведения",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField("Текст обзора")
    author = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.IntegerField(
        "Оценка произведения",
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=10),
        ],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    @staticmethod
    def calc_average_score():
        return Review.objects.aggregate(models.Avg("score"))["score__avg"] or 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.title.rating = self.calc_average_score()
        self.title.save()

    class Meta:
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name="ID обзора",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        return self.text
