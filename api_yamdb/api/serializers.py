import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Genre, Category, Review, Comment


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
        fields = ["id", "title", "text", "author", "score", "pub_date"]
        read_only_fields = ["title"]

    def validate(self, data):
        author = self.context["request"].user
        title_id = self.context["view"].kwargs.get("title_id")
        if (
            self.instance is None
            and Review.objects.filter(
                title_id=title_id, author=author
            ).exists()
        ):
            raise serializers.ValidationError(
                "Вы уже написали обзор на данное произведение."
            )
        return data

    def to_representation(self, instance):
        """Удаление поля title из response"""
        title = super().to_representation(instance)
        title.pop("title", None)
        return title


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ["id", "review", "text", "author", "pub_date"]
        model = Comment
        read_only_fields = ["review"]
