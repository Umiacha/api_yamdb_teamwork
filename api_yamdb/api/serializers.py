import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

<<<<<<< HEAD
from reviews.models import Title, Genre, Category
=======
from reviews.models import Title, Genre, Category, Review, Comment
>>>>>>> 8ca527360eb8664ef87b20607b703d98f1608690


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    genre = GenreSerializer(many=True, required=False)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def validate_year(self, value):
        this_year = dt.date.today().year
        if value > this_year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения, которые еще не вышли!"
            )


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Review
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=["title", "author"],
                message="Ошибка, Вы уже добавили обзор на произведение",
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("review",)
