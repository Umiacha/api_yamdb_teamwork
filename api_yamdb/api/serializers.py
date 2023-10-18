import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from reviews.models import Title, Genre, Category, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects.all())],
    )

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategoryForTitleSerializer(CategorySerializer):
    slug = serializers.CharField()
    name = serializers.CharField(required=False)


class GenreForTitlleSerializer(GenreSerializer):
    slug = serializers.CharField()
    name = serializers.CharField(required=False)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )

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
        return value

    def to_representation(self, instance):
        title_obj = super().to_representation(instance)
        category_name = Category.objects.get(slug=title_obj.get("category"))
        title_obj["category"] = {
            "name": category_name.name,
            "slug": title_obj.get("category"),
        }
        genre_slugs = title_obj.get("genre")
        genres = Genre.objects.filter(slug__in=genre_slugs)
        title_obj["genre"] = [
            {"name": genre.name, "slug": genre.slug} for genre in genres
        ]
        return title_obj


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
