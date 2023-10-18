from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as rest_framework_filters

from reviews.models import Title, Comment, Review, Genre, Category
from .serializers import (
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
)
from users.permissions import AdminOrReadOnly, OwnerOrStaffOrReadOnly


class TitleFilter(rest_framework_filters.FilterSet):
    genre = rest_framework_filters.CharFilter(field_name="genre__slug")
    category = rest_framework_filters.CharFilter(field_name="category__slug")
    year = rest_framework_filters.CharFilter(field_name="year")
    name = rest_framework_filters.CharFilter(field_name="name")

    class Meta:
        model = Title
        fields = ("genre", "category", "year", "name")


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ["get", "post", "patch", "delete", "head"]


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ["name"]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrStaffOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete", "head"]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrStaffOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete", "head"]

    def get_review(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return get_object_or_404(
            Review, pk=self.kwargs.get("review_id"), title=title
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
