from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
