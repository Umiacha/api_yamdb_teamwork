from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    year = models.IntegerField(
        "Год выпуска",
        validators=[MaxValueValidator(timezone.now().year)],
    )
    rating = models.IntegerField("Рейтинг произведения", default=0)
    description = models.TextField("Описание", null=True, blank=True)
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
        on_delete=models.CASCADE,
        related_name="rewiews",
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.FloatField(
        validators=[
            MinValueValidator(limit_value=0.0),
            MaxValueValidator(limit_value=10.0),
        ]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    @staticmethod
    def calc_average_score():
        return Review.objects.aggregate(models.Avg("score"))["score__avg"] or 0

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text
