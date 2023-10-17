import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import (
    UniqueTogetherValidator, UniqueValidator
)

from reviews.models import Title, Genre, Category, Review, Comment, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Category.objects.all()
        )]
    )

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(
            queryset=Genre.objects.all()
        )]
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
    genre = GenreForTitlleSerializer(many=True)
    category = CategoryForTitleSerializer()

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

    def to_internal_value(self, data):
        genre_data = data.get("genre")
        category_data = data.get("category")
        if category_data:
            category_objects = Category.objects.get(slug=category_data)
            category_list = CategorySerializer(category_objects).data
            data["category"] = category_list
        if genre_data:
            genre_objects = Genre.objects.filter(slug__in=genre_data)
            genre_list = GenreSerializer(genre_objects, many=True).data
            data["genre"] = genre_list
        return super().to_internal_value(data)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        category_data = validated_data.pop('category')
        print(category_data.get('slug'))
        category = Category.objects.filter(slug=category_data.get('slug')).first()
        print(category)
        title = Title.objects.create(**validated_data, category=category)
        for genre in genres:
            current_genre = Genre.objects.get(slug=genre.get('slug'))
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Review
        fields = "__all__" # потом надо явно указать поля
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
        fields = "__all__" # потом надо явно указать поля
        model = Comment
        read_only_fields = ("review",)
