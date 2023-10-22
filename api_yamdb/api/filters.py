from django_filters import rest_framework as rest_framework_filters

from reviews.models import Title


class TitleFilter(rest_framework_filters.FilterSet):
    genre = rest_framework_filters.CharFilter(field_name="genre__slug")
    category = rest_framework_filters.CharFilter(field_name="category__slug")
    year = rest_framework_filters.CharFilter(field_name="year")
    name = rest_framework_filters.CharFilter(field_name="name")

    class Meta:
        model = Title
        fields = ("genre", "category", "year", "name")
